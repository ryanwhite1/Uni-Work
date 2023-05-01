# Data from https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population
# Retrieved 2023-04-25

V_ = {}

def council(j, s):
    if j == L[-1]:
        return (abs(s - target[j]), s, 0)
    if (j, s) not in V_:
        minMax = (seats, None)
        for a in range(0, s+1):
            y = (max([abs(a - target[j]), council(j+1, s - a)[0]]), a, s-a)
            if y < minMax:
                minMax = y
        V_[j, s] = minMax
    return V_[j, s]

def representatives():
    s = seats
    print("The smallest maximum discrepancy is", council(0, seats)[0])
    for l in L:
        print(lgas[l][0], council(l, s)[1])
        s = council(l, s)[2]

lgas = [
    ['City of Brisbane', 1272461],
    ['City of Gold Coast', 643461],
    ['Moreton Bay Region', 486645],
    ['City of Blacktown', 387104],
    ['City of Canterbury-Bankstown', 378425],
    ['City of Casey', 368861],
    ['City of Logan', 348020],
    ['Central Coast Council', 347158],
    ['Sunshine Coast Region', 343590],
    ['City of Wyndham', 289571],
    ['Northern Beaches Council', 272184],
    ['City of Greater Geelong', 269508],
    ['City of Parramatta', 258799],
    ['City of Hume', 243738],
    ['City of Sydney', 242237],
    ['Cumberland Council', 239834],
    ['City of Whittlesea', 237932],
    ['City of Ipswich', 236708],
    ['City of Liverpool', 234917],
    ['Sutherland Shire', 234275],
    ['City of Stirling', 223260],
    ['City of Wollongong', 220659],
    ['City of Penrith', 219173],
    ['City of Wanneroo', 215878],
    ['City of Lake Macquarie', 210031],
    ['City of Fairfield', 207922],
    ['City of Brimbank', 201680],
    ['Inner West Council', 199759],
    ['City of Townsville', 197992],
    ['City of Monash', 197980],
    ['The Hills Shire', 188557],
    ['City of Merri-bek', 184707],
    ['Bayside Council', 182369],
    ['City of Melton', 179107],
    ['City of Boroondara', 176632],
    ['City of Whitehorse', 175970],
    ['City of Onkaparinga', 175711],
    ['City of Campbelltown', 175687],
    ['Toowoomba Region', 171135],
    ['City of Melbourne', 169860],
    ['City of Newcastle', 168880],
    ['Shire of Mornington Peninsula', 168865],
    ['Cairns Region', 168853],
    ['City of Kingston', 164680],
    ['City of Greater Dandenong', 163266],
    ['City of Knox', 162769],
    ['City of Darebin', 162501],
    ['Redland City', 161463],
    ['City of Joondalup', 160579],
    ['Georges River Council', 159266]
]

L = range(len(lgas))

seats = 100
population = sum(lgas[i][1] for i in L)
target = [lgas[i][1]*seats/population for i in L]


# print(council(1, 100))

