"""Small teaching helpers for the simplified Week 12 recommender practical.

The point of this module is to keep the practical focused on recommender ideas
instead of dataframe plumbing or recommender library APIs.
"""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from collections.abc import Iterable

import networkx as nx
import numpy as np
import pandas as pd


def load_toy_items() -> pd.DataFrame:
    """Return a tiny catalogue with human-readable item features."""
    return pd.DataFrame(
        [
            {
                "item_id": "space_quest",
                "title": "Space Quest",
                "tags": "space adventure funny",
            },
            {
                "item_id": "dragon_school",
                "title": "Dragon School",
                "tags": "fantasy adventure funny",
            },
            {
                "item_id": "slow_crime",
                "title": "Slow Crime",
                "tags": "mystery gentle drama",
            },
            {
                "item_id": "baking_show",
                "title": "Baking Show",
                "tags": "gentle food comfort",
            },
            {
                "item_id": "moon_garden",
                "title": "Moon Garden",
                "tags": "space gentle drama",
            },
            {
                "item_id": "robot_detective",
                "title": "Robot Detective",
                "tags": "space mystery adventure",
            },
            {
                "item_id": "haunted_bakery",
                "title": "Haunted Bakery",
                "tags": "mystery food funny",
            },
            {
                "item_id": "football_final",
                "title": "Football Final",
                "tags": "sport documentary tense",
            },
        ]
    )


def load_toy_ratings() -> pd.DataFrame:
    """Return known ratings in long format: one row per known user-item rating."""
    rows = [
        ("Asha", "space_quest", 5),
        ("Asha", "dragon_school", 5),
        ("Asha", "slow_crime", 1),
        ("Asha", "baking_show", 2),
        ("Asha", "robot_detective", 4),
        ("Ben", "space_quest", 4),
        ("Ben", "dragon_school", 5),
        ("Ben", "slow_crime", 2),
        ("Ben", "haunted_bakery", 2),
        ("Chris", "space_quest", 1),
        ("Chris", "slow_crime", 5),
        ("Chris", "baking_show", 4),
        ("Chris", "haunted_bakery", 5),
        ("Chris", "football_final", 3),
        ("Dana", "dragon_school", 1),
        ("Dana", "slow_crime", 5),
        ("Dana", "baking_show", 5),
        ("Dana", "moon_garden", 4),
        ("Eli", "space_quest", 3),
        ("Eli", "robot_detective", 5),
        ("Eli", "football_final", 5),
        ("Eli", "slow_crime", 2),
        ("Fiona", "baking_show", 4),
        ("Fiona", "haunted_bakery", 4),
        ("Fiona", "moon_garden", 5),
        ("Fiona", "football_final", 1),
    ]
    return pd.DataFrame(rows, columns=["user", "item_id", "rating"])


def load_toy_likes(
    ratings: pd.DataFrame | None = None,
    min_rating: float = 4,
) -> pd.DataFrame:
    """Return high ratings as user-item links for graph examples."""
    source = load_toy_ratings() if ratings is None else ratings
    likes = source.loc[source["rating"] >= min_rating, ["user", "item_id", "rating"]]
    return likes.reset_index(drop=True)


def ratings_matrix(ratings: pd.DataFrame) -> pd.DataFrame:
    """Return a readable user-item ratings matrix."""
    return ratings.pivot_table(
        index="user",
        columns="item_id",
        values="rating",
        aggfunc="mean",
    )


def recommend_by_popularity(
    ratings: pd.DataFrame,
    items: pd.DataFrame | None = None,
    user: str | None = None,
    top_n: int = 5,
) -> pd.DataFrame:
    """Recommend highest-average items, optionally excluding items a user rated."""
    candidates = ratings.copy()
    if user is not None:
        seen = set(candidates.loc[candidates["user"] == user, "item_id"])
        candidates = candidates.loc[~candidates["item_id"].isin(seen)]

    recs = (
        candidates.groupby("item_id")["rating"]
        .agg(score="mean", ratings_seen="count")
        .reset_index()
        .sort_values(["score", "ratings_seen", "item_id"], ascending=[False, False, True])
    )
    recs["reason"] = recs.apply(
        lambda row: f"average rating {row['score']:.2f} from {int(row['ratings_seen'])} known ratings",
        axis=1,
    )
    return _with_titles(recs.head(top_n), items)


def recommend_by_content(
    items: pd.DataFrame,
    liked_items: Iterable[str],
    top_n: int = 5,
) -> pd.DataFrame:
    """Recommend items with tags overlapping the liked items."""
    liked_ids = _resolve_item_ids(items, liked_items)
    liked_tags: set[str] = set()
    for tags in items.loc[items["item_id"].isin(liked_ids), "tags"]:
        liked_tags.update(str(tags).split())

    rows = []
    for _, item in items.iterrows():
        if item["item_id"] in liked_ids:
            continue
        item_tags = set(str(item["tags"]).split())
        shared = sorted(liked_tags & item_tags)
        union = liked_tags | item_tags
        score = len(shared) / len(union) if union else 0.0
        rows.append(
            {
                "item_id": item["item_id"],
                "title": item["title"],
                "score": score,
                "reason": "shares " + ", ".join(shared) if shared else "no shared tags",
            }
        )
    return (
        pd.DataFrame(rows)
        .sort_values(["score", "title"], ascending=[False, True])
        .head(top_n)
        .reset_index(drop=True)
    )


def user_similarity(ratings: pd.DataFrame, user: str) -> pd.DataFrame:
    """Compare one user to all other users using overlap in known ratings."""
    matrix = ratings_matrix(ratings)
    if user not in matrix.index:
        raise ValueError(f"Unknown user: {user}")

    target = matrix.loc[user]
    rows = []
    for other_user, other in matrix.drop(index=user).iterrows():
        overlap = target.notna() & other.notna()
        n_overlap = int(overlap.sum())
        if n_overlap == 0:
            similarity = 0.0
            mean_gap = math.nan
        else:
            mean_gap = float((target[overlap] - other[overlap]).abs().mean())
            similarity = 1 / (1 + mean_gap)
        rows.append(
            {
                "other_user": other_user,
                "similarity": similarity,
                "shared_ratings": n_overlap,
                "mean_rating_gap": mean_gap,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["similarity", "shared_ratings", "other_user"],
        ascending=[False, False, True],
    )


def recommend_by_similar_users(
    ratings: pd.DataFrame,
    items: pd.DataFrame,
    user: str,
    top_n: int = 5,
) -> pd.DataFrame:
    """Recommend unseen items using ratings from similar users."""
    matrix = ratings_matrix(ratings)
    if user not in matrix.index:
        raise ValueError(f"Unknown user: {user}")

    sims = user_similarity(ratings, user)
    seen = set(ratings.loc[ratings["user"] == user, "item_id"])
    rows = []

    for item_id in matrix.columns:
        if item_id in seen:
            continue
        weighted_sum = 0.0
        weight_total = 0.0
        contributors = []

        for _, sim_row in sims.iterrows():
            other_user = sim_row["other_user"]
            rating = matrix.loc[other_user, item_id]
            if pd.isna(rating) or sim_row["similarity"] <= 0:
                continue
            weighted_sum += float(sim_row["similarity"]) * float(rating)
            weight_total += float(sim_row["similarity"])
            contributors.append(f"{other_user} rated it {rating:.0f}")

        if weight_total == 0:
            continue

        score = weighted_sum * weight_total
        rows.append(
            {
                "item_id": item_id,
                "score": score,
                "reason": "; ".join(contributors[:2]),
            }
        )

    recs = pd.DataFrame(rows).sort_values(["score", "item_id"], ascending=[False, True])
    return _with_titles(recs.head(top_n), items)


def build_user_item_graph(
    likes: pd.DataFrame,
    items: pd.DataFrame | None = None,
) -> nx.Graph:
    """Build a bipartite graph from user-item likes."""
    graph = nx.Graph()
    title_lookup = _title_lookup(items)

    for user in sorted(likes["user"].unique()):
        graph.add_node(user, kind="user", bipartite="user", label=user)

    for item_id in sorted(likes["item_id"].unique()):
        graph.add_node(
            item_id,
            kind="item",
            bipartite="item",
            title=title_lookup.get(item_id, item_id),
            label=title_lookup.get(item_id, item_id),
        )

    for row in likes.itertuples(index=False):
        graph.add_edge(row.user, row.item_id, rating=float(row.rating))

    return graph


def graph_summary(graph: nx.Graph) -> pd.DataFrame:
    """Summarise a user-item graph in a small dataframe."""
    users = [node for node, data in graph.nodes(data=True) if data.get("kind") == "user"]
    item_nodes = [node for node, data in graph.nodes(data=True) if data.get("kind") == "item"]
    return pd.DataFrame(
        [
            {
                "users": len(users),
                "items": len(item_nodes),
                "likes": graph.number_of_edges(),
                "connected_components": nx.number_connected_components(graph),
            }
        ]
    )


def item_projection(likes: pd.DataFrame, items: pd.DataFrame | None = None) -> nx.Graph:
    """Project the user-item graph into an item-item graph."""
    graph = build_user_item_graph(likes, items)
    item_nodes = [
        node for node, data in graph.nodes(data=True) if data.get("kind") == "item"
    ]
    return nx.bipartite.weighted_projected_graph(graph, item_nodes)


def projection_edges(
    likes: pd.DataFrame,
    items: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Return item-item projection edges and their shared-user weights."""
    projection = item_projection(likes, items)
    title_lookup = _title_lookup(items)
    rows = []
    for item_a, item_b, data in projection.edges(data=True):
        rows.append(
            {
                "item_a": item_a,
                "title_a": title_lookup.get(item_a, item_a),
                "item_b": item_b,
                "title_b": title_lookup.get(item_b, item_b),
                "shared_users": int(data.get("weight", 1)),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["shared_users", "title_a", "title_b"],
        ascending=[False, True, True],
    ).reset_index(drop=True)


def related_items_from_projection(
    likes: pd.DataFrame,
    item: str,
    items: pd.DataFrame | None = None,
    top_n: int = 5,
) -> pd.DataFrame:
    """Find items related to one item in the projected item graph."""
    item_id = next(iter(_resolve_item_ids(items, [item]))) if items is not None else item
    projection = item_projection(likes, items)
    title_lookup = _title_lookup(items)

    if item_id not in projection:
        return pd.DataFrame(columns=["item_id", "title", "shared_users", "reason"])

    rows = []
    for neighbour, data in projection[item_id].items():
        shared_users = int(data.get("weight", 1))
        rows.append(
            {
                "item_id": neighbour,
                "title": title_lookup.get(neighbour, neighbour),
                "shared_users": shared_users,
                "reason": f"{shared_users} user(s) liked both items",
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["shared_users", "title"],
        ascending=[False, True],
    ).head(top_n).reset_index(drop=True)


def recommend_by_shared_neighbours(
    likes: pd.DataFrame,
    items: pd.DataFrame,
    user: str,
    top_n: int = 5,
    penalise_popularity: bool = False,
) -> pd.DataFrame:
    """Recommend unseen items by counting paths through related items."""
    seen = set(likes.loc[likes["user"] == user, "item_id"])
    if not seen:
        raise ValueError(f"No likes found for user: {user}")

    projection = item_projection(likes, items)
    title_lookup = _title_lookup(items)
    scores: Counter[str] = Counter()
    evidence: dict[str, list[str]] = defaultdict(list)

    for liked_item in seen:
        if liked_item not in projection:
            continue
        for candidate, data in projection[liked_item].items():
            if candidate in seen:
                continue
            weight = int(data.get("weight", 1))
            scores[candidate] += weight
            evidence[candidate].append(
                f"{weight} shared user(s) with {title_lookup.get(liked_item, liked_item)}"
            )

    rows = []
    for candidate, raw_score in scores.items():
        popularity = max(projection.degree(candidate), 1)
        score = raw_score / popularity if penalise_popularity else float(raw_score)
        rows.append(
            {
                "item_id": candidate,
                "title": title_lookup.get(candidate, candidate),
                "score": score,
                "raw_path_count": int(raw_score),
                "item_degree": popularity,
                "reason": "; ".join(evidence[candidate][:3]),
            }
        )

    return pd.DataFrame(rows).sort_values(
        ["score", "raw_path_count", "title"],
        ascending=[False, False, True],
    ).head(top_n).reset_index(drop=True)


def random_walk_recommendations(
    likes: pd.DataFrame,
    items: pd.DataFrame,
    user: str,
    walks: int = 1000,
    seed: int = 42,
    top_n: int = 5,
) -> pd.DataFrame:
    """Recommend by sampling user -> item -> user -> item paths."""
    graph = build_user_item_graph(likes, items)
    if user not in graph:
        raise ValueError(f"No likes found for user: {user}")

    rng = random.Random(seed)
    seen = sorted(
        node
        for node in graph.neighbors(user)
        if graph.nodes[node].get("kind") == "item"
    )
    if not seen:
        raise ValueError(f"No liked items found for user: {user}")

    endpoints = []
    for _ in range(walks):
        first_item = rng.choice(seen)
        other_users = sorted(
            node
            for node in graph.neighbors(first_item)
            if node != user and graph.nodes[node].get("kind") == "user"
        )
        if not other_users:
            continue

        other_user = rng.choice(other_users)
        candidate_items = sorted(
            node
            for node in graph.neighbors(other_user)
            if node not in seen and graph.nodes[node].get("kind") == "item"
        )
        if not candidate_items:
            continue
        endpoints.append(rng.choice(candidate_items))

    counts = Counter(endpoints)
    successful_walks = max(len(endpoints), 1)
    title_lookup = _title_lookup(items)
    rows = [
        {
            "item_id": item_id,
            "title": title_lookup.get(item_id, item_id),
            "visits": visits,
            "score": visits / successful_walks,
            "reason": f"visited {visits} time(s) in {len(endpoints)} successful walks",
        }
        for item_id, visits in counts.items()
    ]
    return pd.DataFrame(rows).sort_values(
        ["visits", "title"],
        ascending=[False, True],
    ).head(top_n).reset_index(drop=True)


def hide_known_like(
    likes: pd.DataFrame,
    user: str = "Ben",
    item_id: str = "dragon_school",
) -> tuple[pd.DataFrame, pd.Series]:
    """Hide one known like for ranking evaluation."""
    mask = (likes["user"] == user) & (likes["item_id"] == item_id)
    if not mask.any():
        raise ValueError(f"No known like for user={user!r}, item_id={item_id!r}")
    hidden = likes.loc[mask].iloc[0]
    train = likes.loc[~mask].reset_index(drop=True)
    return train, hidden


def score_hidden_like(
    recommendations: pd.DataFrame,
    hidden: pd.Series,
    k: int = 5,
) -> pd.DataFrame:
    """Check whether a hidden liked item appears in a recommendation list."""
    item_id = hidden["item_id"]
    if recommendations.empty or item_id not in set(recommendations["item_id"]):
        return pd.DataFrame(
            [
                {
                    "item_id": item_id,
                    "rank": np.nan,
                    "score": np.nan,
                    f"hit_at_{k}": False,
                    "note": "hidden item was not recommended",
                }
            ]
        )

    row_number = recommendations.index[recommendations["item_id"] == item_id][0]
    match = recommendations.loc[row_number]
    rank = int(row_number) + 1
    return pd.DataFrame(
        [
            {
                "item_id": item_id,
                "rank": rank,
                "score": float(match["score"]),
                f"hit_at_{k}": rank <= k,
                "note": "lower rank is better",
            }
        ]
    )


def hide_known_rating(
    ratings: pd.DataFrame,
    user: str = "Ben",
    item_id: str = "slow_crime",
) -> tuple[pd.DataFrame, pd.Series]:
    """Hide one known rating so students can test a recommendation method."""
    mask = (ratings["user"] == user) & (ratings["item_id"] == item_id)
    if not mask.any():
        raise ValueError(f"No known rating for user={user!r}, item_id={item_id!r}")
    hidden = ratings.loc[mask].iloc[0]
    train = ratings.loc[~mask].reset_index(drop=True)
    return train, hidden


def score_hidden_rating(predictions: pd.DataFrame, hidden: pd.Series) -> pd.DataFrame:
    """Compare a prediction table with one hidden rating."""
    match = predictions.loc[predictions["item_id"] == hidden["item_id"]]
    if match.empty:
        return pd.DataFrame(
            [
                {
                    "item_id": hidden["item_id"],
                    "actual_rating": hidden["rating"],
                    "predicted_score": np.nan,
                    "absolute_error": np.nan,
                    "note": "hidden item was not recommended",
                }
            ]
        )

    predicted = float(match.iloc[0]["score"])
    actual = float(hidden["rating"])
    return pd.DataFrame(
        [
            {
                "item_id": hidden["item_id"],
                "actual_rating": actual,
                "predicted_score": predicted,
                "absolute_error": abs(actual - predicted),
                "note": "lower absolute error is better",
            }
        ]
    )


def _resolve_item_ids(items: pd.DataFrame, values: Iterable[str]) -> set[str]:
    lookup = {}
    for _, row in items.iterrows():
        lookup[str(row["item_id"]).lower()] = row["item_id"]
        lookup[str(row["title"]).lower()] = row["item_id"]

    resolved = set()
    for value in values:
        key = str(value).lower()
        if key not in lookup:
            raise ValueError(f"Unknown item: {value}")
        resolved.add(lookup[key])
    return resolved


def _title_lookup(items: pd.DataFrame | None) -> dict[str, str]:
    if items is None:
        return {}
    return dict(zip(items["item_id"], items["title"], strict=False))


def _with_titles(recs: pd.DataFrame, items: pd.DataFrame | None) -> pd.DataFrame:
    if items is None or recs.empty or "title" in recs.columns:
        return recs.reset_index(drop=True)
    titled = recs.merge(items[["item_id", "title"]], on="item_id", how="left")
    columns = ["item_id", "title"] + [c for c in titled.columns if c not in {"item_id", "title"}]
    return titled[columns].reset_index(drop=True)
