# Created by: Justin Sliech
# Created On: 11/15/2026
# Description: Provides functions for searching, filtering, and sorting collections of data.

def search_data(data, search_term):
    """Search records for items containing the search term"""

    # Return all records if no search term was provided.
    if not search_term:
        return data

    results = []

    # Check each field in every record for the search term.
    for item in data:
        for value in item.values():
            if search_term.lower() in str(value).lower():
                results.append(item)
                break

    return results

def filter_data(data, filters):
    """Filter records using exact field values."""

    # Return all records if no filters were provided.
    if not filters:
        return data

    results = []

    # Check whether each record matches all filter criteria.
    for item in data:
        matches = True

        for key, value in filters.items():
            if key not in item or item[key] != value:
                matches = False
                break

        if matches:
            results.append(item)

    return results

def sort_data(data, sort_by, order="ascending"):
    """Sort records by a selected field."""

    # Return an empty list if there are no records.
    if not data:
        return []

    # Check whether the sort order is valid.
    if order not in ("ascending", "descending"):
        raise ValueError("Sort order must be ascending or descending.")

    # Check whether the selected field exists in the records.
    if sort_by not in data[0]:
        raise ValueError("Sort field does not exist.")

    # Sort records based on the selected field.
    return sorted(data, key=lambda item: item[sort_by],
                  reverse=(order == "descending"))