MESSAGE_MATCH = 'Match'
MESSAGE_MATCH_WITH_EXCEPTION = 'Match With Exceptions'
MESSAGE_NO_MATCH = 'No Match'

ENHANCED_NO_MATCH = 'none'
ENHANCED_POSTAL_MATCH = 'postal-match'
ENHANCED_NON_POSTAL_MATCH = 'non-postal-match'
ENHANCED_MISSING_SECONDARY = 'missing-secondary'
ENHANCED_UNKNOWN_SECONDARY = 'unknown-secondary'
ENHANCED_IGNORED_INPUT = 'ignored-input'

DPV_MILITARY_MATCH = 'F1'
DPV_BOX_NUMBER_MISSING = 'P1'
DPV_CONFIRMED_PMB = 'RR'
DPV_CONFIRMED_WITHOUT_PMB = 'R1'
DPV_PHANTOM_CARRIER_ROUTE = 'R7'
DPV_UNIQUE_ZIP_CODE = 'U1'
DPV_TRAILING_ALPHA = 'TA'

_dpv_exception_set = {
	DPV_MILITARY_MATCH,
	DPV_BOX_NUMBER_MISSING,
	DPV_CONFIRMED_PMB,
	DPV_CONFIRMED_WITHOUT_PMB,
	DPV_PHANTOM_CARRIER_ROUTE,
	DPV_UNIQUE_ZIP_CODE,
	DPV_TRAILING_ALPHA,
}


def _has_dpv_footnote_exceptions(dpv_footnotes: str) -> bool:
	if dpv_footnotes is None:
		return False
	return any(dpv_footnotes[i:i+2] in _dpv_exception_set for i in range(0, len(dpv_footnotes) - 1, 2))


def _enhanced_match_summary(enhanced_match: str, dpv_footnotes: str) -> str:
	is_postal_match = False
	has_enhanced_exception = False
	for val in enhanced_match.split(','):
		if val in (ENHANCED_POSTAL_MATCH, ENHANCED_NON_POSTAL_MATCH):
			is_postal_match = True
		elif val in (ENHANCED_MISSING_SECONDARY, ENHANCED_UNKNOWN_SECONDARY, ENHANCED_IGNORED_INPUT):
			has_enhanced_exception = True
	if not is_postal_match:
		return MESSAGE_NO_MATCH
	if has_enhanced_exception or _has_dpv_footnote_exceptions(dpv_footnotes):
		return MESSAGE_MATCH_WITH_EXCEPTION
	return MESSAGE_MATCH


def _dpv_match_code_summary(dpv_match_code: str, dpv_footnotes: str) -> str:
	if dpv_match_code == 'Y':
		return MESSAGE_MATCH_WITH_EXCEPTION if _has_dpv_footnote_exceptions(dpv_footnotes) else MESSAGE_MATCH
	if dpv_match_code in ('S', 'D'):
		return MESSAGE_MATCH_WITH_EXCEPTION
	return MESSAGE_NO_MATCH


def summary(enhanced_match: str, dpv_match_code: str, dpv_footnotes: str) -> str:
	if enhanced_match:
		return _enhanced_match_summary(enhanced_match, dpv_footnotes)
	return _dpv_match_code_summary(dpv_match_code, dpv_footnotes)
