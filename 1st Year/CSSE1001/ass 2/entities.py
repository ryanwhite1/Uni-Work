"""
    Entity classes used in the second assignment for CSSE1001/7030.

    Athlete: Details of an athlete participating at the games.
    Event: Details of an individual event at the games.
    Country: Details of a country and its delegation at the games.
    Result: An athlete's result in an event.
"""

__author__ = "Ryan White 44990392"
__email__ = "s4499039@uq.edu.au"



class Athlete(object) :
    """Details of an athlete who is competing at the games."""
    
    def __init__(self, identifier, first_name, surname, country) :
        """
        Parameters:
            identifier (str): Athlete's identification number
            first_name (str): Athlete's first name.
            surname (str): Athlete's surname.
            country (Country): Object representing this athlete's country.
        """
        self._identifier = identifier
        self._first_name = first_name
        self._surname = surname
        self._country = country
        self._events = []

    def get_result(self, event) :
        """Return the result the athlete obtained in 'event'.

        Parameters:
            event (Event): Event for which the athlete's result is wanted.
            
        Return:
            Result: Athlete's result in 'event'.
        """
        pass

    def add_result(self, event, result) :
        """Sets athlete's 'result' in 'event', overwriting if previously set.

        Parameters:
            event (Event): Event in which this athlete competed.
            result (Result): Final result obtained in event.
        """
        pass
        
    def add_event(self, event) :
        """Adds event to those in which this athlete will compete.

        Parameters:
            event (Event): Event in which this athlete will compete.
        """
        self._events.append(event)
        
    def add_events(self, events) :
        """Adds all events to those in which this athlete will compete.

        Parameters:
            events (list[Event]): List of events in which this athlete will compete.
        """
        for event in events:
            self._events.append(event)
        
        
    def get_events(self) :
        """(list[Event]) All events in which this athlete is competing."""
        return self._events

    def get_id(self) :
        """(str) Athlete's identification number."""
        return str(self._identifier)
    
    def get_full_name(self) :
        """(str) Athlete's full name (first + surname)."""
        return str(self._first_name) + str(self._surname)

    def get_country(self) :
        """(Country) Country delegation to which this Athlete belongs."""
        return self._country

    def __str__(self) :
        return ""



class Result(object) :
    """An athlete's result in an event."""
    
    def __init__(self, result_value) :
        """
        Parameters:
            result_value (float): Time or score athlete achieved in event.
        """
        self._result_value = result_value

    def get_place(self) :
        """(str) Place athlete obtained in the final event.

        Raise:
            RuntimeError: if places not yet determined.
        """
        try:
            return self._result_value
        except:
            raise RuntimeError

    def set_place(self, place) :
        """Sets the place that the athlete achieved in the final event.

        Parameters:
            place (int): Place that athlete achieved in the event.
        """
        pass

    def places_determined(self) :
        """(bool) Has places been determined yet or not."""
        pass
    
    def get_result(self) :
        """(str) Time or score athlete achieved in the final event."""
        return self._result_value

    def get_medal(self) :
        """(str) Medal athlete achieved or empty string if no medal.

        Raise:
            RuntimeError: if places not yet determined.
        """
        pass

    def __str__(self) :
        return ""


class Event(object) :
    """An event in which athletes compete."""
    
    def __init__(self, event_name, timed, athletes) :
        """
        Parameters:
            event_name (str): Official name of this event.
            timed (bool): Indicates if this is a timed event (else scored).
            athletes (list[Athlete]): Athletes who will compete in this event.
        """
        self._event_name = event_name
        self._timed = timed
        self._athletes = athletes
        
    def is_timed(self) :
        """(bool) True if event is timed, False if event is scored."""
        return self._timed
        
    def get_name(self) :
        """(str) Official name of this event."""
        return self._event_name
        
    def get_athletes(self) :
        """(list[Athlete]) All athletes currently registered to compete
                           in this event.
        """
        return self._athletes
        
    def add_athlete(self, athlete) :
        """Adds athlete to those who will compete in this event.

        Parameters:
            athlete (Athlete): An athlete who will compete in this event.
        """
        self._athletes.append(athlete)
        
    def add_athletes(self, athletes) :
        """Adds all athletes to those who will compete in this event.

        Parameters:
            athletes (list[Athlete]): List of athletes who will compete
                                      in this event.
        """
        for athlete in athletes:
            self._athletes.append(athlete)

    def __str__(self) :
        return ""



class Country(object) :
    """Representation of a country's delegation."""

    def __init__(self, country_name, country_code) :
        """
        Parameters:
            country_name (str): Official name of this country.
            country_code (str): 3 letter code used to represent this country.
        """
        self._country_name = country_name
        self._country_code = country_code
        self._athletes = []
        

    def get_athletes(self) :
        """(list[Athlete]) All athletes competing for this country."""
        return self._athletes
        
    def add_athlete(self, athlete) :
        """Adds athlete as a member of this country's delegation.

        Parameters:
            athlete (Athlete): An athlete who will compete for this country.
        """
        self._athletes.append(athlete)
        
    def add_athletes(self, athletes) :
        """Adds all athletes as members of this country's delegation.

        Parameters:
            athletes (list[Athlete]): List of athletes who will compete
                                      for this country.
        """
        for athlete in athletes:
            self._athletes.append(athlete)

    def get_name(self) :
        """(str) Country's official name."""
        return self._country_name

    def get_country_code(self) :
        """(str) Country's 3 letter representation code."""
        return self._country_code

    def __str__(self) :
        return ""



class ManagedDictionary(object) :
    """A generic collection as a managed dictionary."""

    def __init__(self) :
        self._items = {}

    def add_item(self, key, item) :
        """Adds an item to this collection.
           Overwriting previous item if key was mapped to an item already.

        Parameters:
            key (immutable): Unique key for the item.
            item (value): The item to be added to this collection.
        """
        self._items[key] = item
        
    def get_items(self) :
        """(list) All items in this collection."""
        return list(self._items.values())

    def find_item(self, key) :
        """Return the item which corresponds to this key.

        Parameters:
            key (immutable): Unique key for an item.
    
        Return:
            (value): Item that corresponds to this key.

        Raises:
            (KeyError): If 'key' does not correspond to an item.
        """
        try:
            return self._items[key]
        except:
            raise KeyError


"""
    Globally defined collections of all key entity objects.
    These are to be used to store all of each type of entity objects that
    are created by your program.
"""
all_athletes = ManagedDictionary()
all_countries = ManagedDictionary()
all_events = ManagedDictionary()



def load_data(athletes, countries, events,
              timed_events_results, scored_events_results) :
    """Loads the data from the named data files.

    Data is loaded into the all_athletes, all_countries and all_events
    collections. Results are accessible through the objects in these collections.

    Parameters:
        athletes (str) : Name of file containing athlete data.
        countries (str): Name of file containing country data.
        events (str)   : Name of file containing events data.
        timed_events_results (str) : Name of file containing results for timed
                                     events.
        scored_events_results (str): Name of file containing results for scored
                                     events.
    """
    file_athletes = str(athletes + ".csv")
    with open[file_athletes, "r"] as athlete_data:
        for row in athlete_data:
            ident = Athlete.get_id
            name = Athlete.get_full_name
            all_athletes.ManagedDictionary.add_item(ident, name)
        
        



if __name__ == "__main__" :
    print("This module provides the entities for the Olympic games results",
          "processing application and is not meant to be executed on its own.")
