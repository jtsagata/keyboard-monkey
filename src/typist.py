#!/usr/bin/python3
import unicodedata

GreekTypist = {
    'Ά': ['dead_acute', 'Greek_alpha'],
    '·': ['dead_acute', 'period'],
    'Έ': ['dead_acute', 'Greek_epsilon'],
    'Ή': ['dead_acute', 'Greek_eta'],
    'Ί': ['dead_acute', 'Greek_iota'],
    'Ό': ['dead_acute', 'Greek_omicron'],
    'Ύ': ['dead_acute', 'Greek_upsilon'],
    'Ώ': ['dead_acute', 'Greek_omega'],
    'ΐ': ['dead_acute', 'dead_acute', 'Greek_iota'],
    'Α': ['Greek_alpha'],
    'Β': ['Greek_beta'],
    'Γ': ['Greek_gamma'],
    'Δ': ['Greek_delta'],
    'Ε': ['Greek_epsilon'],
    'Ζ': ['Greek_zeta'],
    'Η': ['Greek_eta'],
    'Θ': ['Greek_theta'],
    'Ι': ['Greek_iota'],
    'Κ': ['Greek_kappa'],
    'Λ': ['Greek_lamda'],
    'Μ': ['Greek_mu'],
    'Ν': ['Greek_nu'],
    'Ξ': ['Greek_xi'],
    'Ο': ['Greek_omicron'],
    'Π': ['Greek_pi'],
    'Ρ': ['Greek_rho'],
    'Σ': ['Greek_sigma'],
    'Τ': ['Greek_tau'],
    'Υ': ['Greek_upsilon'],
    'Φ': ['Greek_phi'],
    'Χ': ['Greek_chi'],
    'Ψ': ['Greek_psi'],
    'Ω': ['Greek_omega'],
    'Ϊ': ['dead_acute', 'Greek_iota'],
    'Ϋ': ['dead_acute', 'Greek_upsilon'],
    'ά': ['dead_acute', 'Greek_alpha'],
    'έ': ['dead_acute', 'Greek_epsilon'],
    'ή': ['dead_acute', 'Greek_eta'],
    'ί': ['dead_acute', 'Greek_iota'],
    'ΰ': ['dead_acute', 'Greek_upsilon'],
    'α': ['Greek_alpha'],
    'β': ['Greek_beta'],
    'γ': ['Greek_gamma'],
    'δ': ['Greek_delta'],
    'ε': ['Greek_epsilon'],
    'ζ': ['Greek_zeta'],
    'η': ['Greek_eta'],
    'θ': ['Greek_theta'],
    'ι': ['Greek_iota'],
    'κ': ['Greek_kappa'],
    'λ': ['Greek_lamda'],
    'μ': ['Greek_mu'],
    'ν': ['Greek_nu'],
    'ξ': ['Greek_xi'],
    'ο': ['Greek_omicron'],
    'π': ['Greek_pi'],
    'ρ': ['Greek_rho'],
    'ς': ['Greek_finalsmallsigma'],
    'σ': ['Greek_sigma'],
    'τ': ['Greek_tau'],
    'υ': ['Greek_upsilon'],
    'φ': ['Greek_phi'],
    'χ': ['Greek_chi'],
    'ψ': ['Greek_psi'],
    'ω': ['Greek_omega'],
    'ϊ': ['dead_acute', 'Greek_iota'],
    'ϋ': ['dead_acute', 'Greek_upsilon'],
    'ό': ['dead_acute', 'Greek_omicron'],
    'ύ': ['dead_acute', 'Greek_upsilon'],
    'ώ': ['dead_acute', 'Greek_omega'],
    '΄': ['dead_acute'],
    ',': ['comma']
}


def read_corpus(filename, numchars=100, typist=GreekTypist):
    with open(filename, 'r') as f:
        contents = f.read(numchars)
    # print(contents)

    res = []
    for c in contents:
        if c == '\n':
            continue
        name = unicodedata.name(c)
        if name == 'SPACE':
            res.append('<SPACE>')
            continue
        if c in typist.keys():
            for k in typist[c]:
                res.append(k)
                # else:
                #     print("missing: '{}' {}".format(c,unicodedata.name(c)))
    return res

def get_stroke_for_greek_symbol(symbol,keyboard):
    pass
