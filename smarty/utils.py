class Utils:
    @staticmethod
    def is_ambiguous(result):
        return len(result) > 1

    @staticmethod
    def is_invalid(result):
        if len(result) == 0 or not result[0].analysis:  # TODO: watchme...
            return True

        dpv_match_code = result[0].analysis.dpv_match_code

        exactly_one_result = (len(result) == 1)
        dpv_match_code_is_none = (dpv_match_code == "N")
        address_is_confirmed_in_some_way = dpv_match_code != "N"

        if exactly_one_result:
            if result[0].analysis.enhanced_match:
                enhanced_match = result[0].analysis.enhanced_match.split(",")
                return enhanced_match.find("none") != -1
            elif dpv_match_code_is_none:
                return True
            else:
                return not address_is_confirmed_in_some_way
        else:
            return False

    @staticmethod
    def is_missing_secondary(result):
        if len(result) == 0:  # There were no results
            return False

        enhanced_matching_response = result[0].analysis.enhanced_match

        if enhanced_matching_response:
            has_missing_secondary = enhanced_matching_response.find("missing-secondary")
            has_unknown_secondary = enhanced_matching_response.find("unknown-secondary")

            return has_missing_secondary != -1 or has_unknown_secondary != -1

        n1_dpv_footnote_present = result[0].analysis.dpvFootnotes.find("N1") != -1
        r1_dpv_footnote_present = result[0].analysis.dpvFootnotes.find("R1") != -1
        h_sharp_footnote_present = result[0].analysis.footnotes.find("H#") != -1

        return n1_dpv_footnote_present or r1_dpv_footnote_present or h_sharp_footnote_present

    @staticmethod
    def is_valid(result):
        return not Utils.is_invalid(result)
