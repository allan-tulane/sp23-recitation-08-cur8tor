####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant'), ('AAAGAATTCA', 'AAA---T-CA')]

# For two strings S and T, the Minimum Edit Distance (MED) can be computed by considering the following cases:

# If S is empty, MED is the length of T (all characters of T must be inserted).
# If T is empty, MED is the length of S (all characters of S must be deleted).
# If S[0] is equal to T[0], MED is equal to MED(S[1:], T[1:])
# If S[0] is not equal to T[0], MED is equal to 1 + min(MED(S[1:], T), MED(S, T[1:]))

# This function takes in two strings, S and T as input parameters
def MED(S, T):
    # If first string is empty, the minimum edit distance is the length of the second string
    if (S == ""):
        return(len(T))
    # If the second string is empty, the minimum edit distance is the length of the first string
    elif (T == ""):
        return(len(S))
    else:
        # Case when the first character of both strings match
        if (S[0] == T[0]):
            # Minimum edit distance would be same as that of smaller strings after removing the first characters
            return(MED(S[1:], T[1:]))
        else:
            # When the first characters don't match, find the minimum of the three possible paths - remove first character of T, remove first character of S or replace first character of S with first character of T
            return(1 + min(MED(S, T[1:]), MED(S[1:], T), MED(S[1:], T[1:])))
        

# This function takes in two strings, S and T and a memoization dictionary memo_MED as input parameters
def fast_MED(S, T, memo_MED={}):
    # Check if the result for (S, T) is already present in the memoization dictionary
    if (S, T) in memo_MED:
        return memo_MED[(S, T)]
    # If first string is empty, the minimum edit distance is the length of the second string
    elif (S == ""):
        return(len(T))
    # If the second string is empty, the minimum edit distance is the length of the first string
    elif (T == ""):
        return(len(S))
    else:
        # Case when the first character of both strings match
        if (S[0] == T[0]):
            # Store the result for (S, T) before returning it
            memo_MED[(S, T)] = fast_MED(S[1:], T[1:], memo_MED)
        else:
            # When the first characters don't match, find the minimum of the three possible paths - remove first character of T, remove first character of S or replace first character of S with first character of T. Store the result for (S, T) before returning it
            memo_MED[(S, T)] = 1 + min(fast_MED(S, T[1:], memo_MED), fast_MED(S[1:], T, memo_MED), fast_MED(S[1:], T[1:], memo_MED))
        return memo_MED[(S, T)]


# This function takes in two strings, S and T and two memoization dictionaries, memo_MED and memo_align as input parameters
def fast_align_MED(S, T, memo_MED={}, memo_align={}):
    # Check if the result for (S, T) is already present in the memoization dictionary
    if (S, T) in memo_align:
        return memo_align[(S, T)]
    # If first string is empty, return a tuple with first item being a '-' of length equal to second string and second item being second string. 
    elif (S == ""):
        return ("-" * len(T), T)
    # If the second string is empty, return a tuple with first item being the first string and second item being a '-' of length equal to first string
    elif (T == ""):
        return (S, "-" * len(S))
    else:
        # Case when the first character of both strings match
        if (S[0] == T[0]):
            # Call the function recursively on the remaining string after matching characters
            align_S, align_T = fast_align_MED(S[1:], T[1:], memo_MED, memo_align)
            # Return a tuple with first item being the matching character and the aligned strings as second item
            return (S[0] + align_S, T[0] + align_T)
        else:
            # Calculate the minimum edit distance in all three possible paths - substitution, insertion or deletion
            substitution = fast_MED(S[1:], T[1:], memo_MED)
            insertion = fast_MED(S, T[1:], memo_MED)
            deletion = fast_MED(S[1:], T, memo_MED)

            # Choose the path with minimum edit distance and call function recursively on the selected path. Store the result in memoization dictionary before returning it.
            if insertion <= deletion and insertion <= substitution:
                align_S, align_T = fast_align_MED(S, T[1:], memo_MED, memo_align)
                return ('-' + align_S, T[0] + align_T)
            elif deletion <= insertion and deletion <= substitution:
                align_S, align_T = fast_align_MED(S[1:], T, memo_MED, memo_align)
                return (S[0] + align_S, '-' + align_T)
            else:
                align_S, align_T = fast_align_MED(S[1:], T[1:], memo_MED, memo_align)
                return (S[0] + align_S, T[0] + align_T)


def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)


def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        computed_edit_distance = sum(s != t for s, t in zip(align_S, align_T))
        expected_edit_distance = sum(s != t for s, t in zip(alignments[i][0], alignments[i][1]))
        
        assert computed_edit_distance == expected_edit_distance, f"Expected edit distance: {expected_edit_distance}, Got: {computed_edit_distance}, Alignment: {(align_S, align_T)}"


test_MED()
test_align()