class Utils:
    @staticmethod
    def is_invalid(result):
        if result is None:
            return True
        if result.enhanced_match == "none":
            return True
        return False

    @staticmethod
    def verify_results(result):
        if result.vacant == "Y":
            return "Match-Vacant - The address is valid but vacant."
        if result.active == "N":
            return "Match-Inactive - The address is valid but inactive."
        if result.enhanced_match == "non-postal-match":
            return "Match-Non-Postal - A match was made to a valid non-postal address."
        else:
            return "Valid Match - A valid match was made to a postal address."
