# Email Address Validator
# By Cohen Beveridge
# For Computer Science Specialist Class Year 8 2021
# Last Updated: 24/09/2021

# Description:
# This program features an interactive mode, where the user inputs an email address for validation, and a
# batch mode, where a file name is inputted and a new file is created with the results appended to each line. A list
# of rules can be seen in the documentation. A test file (testfile.txt) has also been included with this program for
# testing the program's batch capabilities. This program uses no imported code except os.path, which is for testing if
# a file is real. This program does NOT check if the address is real, or if it could be created right now. It simply
# checks whether the address could be created in the future with the current rules. If some results contradict some
# sources, please refer to the documentation file for a list of rules which were used for this program.

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Functions begin here
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Function to check length of the email address

def LengthInRange(address):
    length = len(address)
    if length > 255:  # maximum
        return "Address was too long"  # An error message
    elif length < 6:  # minimum
        return "Address was too short"  # Another error message
    else:
        return "valid"  # A valid message

# End function


# Function to check if the email address contains an @ sign

def AddressContainsAt(address):
    return '@' in address  # Returns True if @ symbol is in address

# End function


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# FUNCTIONS DEALING WITH QUOTES AND COMMENTS BEGIN HERE
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Function to determine if character is escaped by an unescaped backslash in a string

def UnBackslashed(string, character):
    backslashes = 0
    if string[character - 1] != '\\':  # Returns True straight away if the character before isn't a backslash
        return True
    for x in range(character):
        if string[character - x - 1] == '\\':   # Checks every character counting backwards
            backslashes += 1
        else:
            break   # If it's not a backslash the loop ends
    return backslashes % 2 == 0  # Backslash amount must be even to be plain/literal

# End function


# A function to find the first quote and the first open bracket

def OpenQuoteAndBracket(address):
    openquote = -1
    openbracket = -1
    for char in range(len(address)):
        if UnBackslashed(address, char):  # A backslashed quote/bracket does not count
            if address[char] == '"' and openquote == -1:
                openquote = char
            if address[char] == '(' and openbracket == -1:
                openbracket = char
    return openquote, openbracket

# End function


# A function to find the closing bracket after knowing the openbracket

def CloseBracket(address, openbracket):
    check = address[openbracket + 1:]       # The string to check
    incomments = 1
    closebracket = -1
    for char in range(len(check)):
        if incomments == 0:     # If the comment has closed, break the loop
            break
        if UnBackslashed(check, char):
            if check[char] == '(':      # The imbalance of comments within comments increases
                incomments += 1
            elif check[char] == ')':    # The imbalance of comments within comments decreases
                incomments -= 1
                closebracket = char
    if closebracket == -1 or incomments != 0:   # Check if parentheses did not match
        return 'invalid'
    else:
        return closebracket + openbracket + 1   # Accounts for the variable 'check' being shorter than the address

# End function


# Function to validate the position of a comment

def CommentPositionValid(address, openbracket, closebracket):   # The start and end of the comment is given
    valid = 0
    if openbracket == 0:
        valid += 1
    elif address[openbracket - 1] == '.' or address[openbracket - 1] == '@':
        valid += 1
    if closebracket == len(address) - 1:
        valid += 1
    elif address[closebracket + 1] == '.' or address[closebracket + 1] == '@':
        valid += 1
    return valid == 1   # One (no more) of the above conditions must be True

# End function


# Function to validate the contents of a comment

def CommentContentsValid(address, openbracket, closebracket):
    comment = address[openbracket + 1:closebracket]     # Creates a string variable which is the contents of the comment
    restricted = ['\t', '\r', '\n']     # Tab, Carriage Return and Line Feed are restricted unless unbackslashed
    for char in range(len(comment)):
        if (not comment[char].isascii()) or (comment[char] in restricted and UnBackslashed(comment, char)):
            return False
    return True

# End function


# Function to replace a quote or comment

def ReplacePart(address, start, end, sort):     # 'sort' is either "q" or "c"
    before = address[:start]
    after = address[end + 1:]
    part = address[start:end + 1]
    length = len(part)
    fillin = sort * length      # E.g. (aa) -> cccc  ||  "aa" -> qqqq
    address = before + fillin + after
    return address

# End function


# Function to remove a comment

def RemoveComment(address, start, end):
    before = address[:start]
    after = address[end + 1:]
    address = before + after
    return address

# End function


# Function to validate everything about comments

def ValidateComments(address, openbracket):
    # Find Closing Parenthesis
    closebracket = CloseBracket(address, openbracket)
    if closebracket == 'invalid':
        return False, 'Parentheses for a comment did not match'

    # Validate position of comments
    if not CommentPositionValid(address, openbracket, closebracket):
        return False, 'Position of a comment was invalid'

    # Validate contents of comments
    if not CommentContentsValid(address, openbracket, closebracket):
        return False, 'Contents of a comment was invalid'

    # Replace comments in address
    newaddress = ReplacePart(address, openbracket, closebracket, 'c')
    return True, newaddress

# End function


# Function to find the closing quotation mark when the opening one is given

def CloseQuote(address, openquote):
    check = address[openquote + 1:]     # A variable with part the of address to check
    closequote = -1
    for char in range(len(check)):
        if UnBackslashed(check, char):
            if check[char] == '"':
                closequote = char
                break
    if closequote == -1:
        return 'invalid'
    else:
        return closequote + openquote + 1

# End function


# Function to validate position of a quote

def QuotePositionValid(address, openquote, closequote):
    if not (address[closequote + 1] == '.' or address[closequote + 1] == '@'):    # What is after the quote
        return False
    if openquote != 0:
        if address[openquote - 1] != '.':   # What is before the quote
            return False
    afterquote = address[closequote + 1:]
    return '@' in afterquote        # There must be an @ after the quote, meaning no quotes in the domain

# End function


# Function to validate the contents of a quote

def QuoteContentsValid(address, openquote, closequote):
    quote = address[openquote + 1:closequote]   # Sets the quote
    restricted = ['\t', '\r', '\n']     # A list of restricted characters
    for char in range(len(quote)):
        if not (quote[char].isascii()) or (quote[char] in restricted and UnBackslashed(quote, char)):
            return False
    return True

# End function


# Function to completely validate a quote

def ValidateQuotes(address, openquote):
    # Find closing quotation mark
    closequote = CloseQuote(address, openquote)
    if closequote == 'invalid':
        return False, 'Quotation marks for a quote did not match'

    # Validate position of quotes
    if not QuotePositionValid(address, openquote, closequote):
        return False, 'Position of a quote was invalid'

    # Validate contents of quotes
    if not QuoteContentsValid(address, openquote, closequote):
        return False, 'Contents of a quote was invalid'

    # Replace quotes in address
    newaddress = ReplacePart(address, openquote, closequote, 'q')
    return True, newaddress

# End function


# Function to validate both quotes and comments simultaneously

def ValidateQuotesComments(address):
    while True:     # An infinite loop is okay, because something will eventually be returned
        openquote, openbracket = OpenQuoteAndBracket(address)  # Assign the opening quote and the opening bracket

        if openquote == -1 and openbracket != -1:  # Comments were found, but not quotes
            validaddress, message = ValidateComments(address, openbracket)
            if validaddress:
                address = message
            else:
                return message

        elif openquote == -1 and openbracket == -1:  # Neither quote not comment exists
            return 'valid'    # Ends the function with a valid outcome
            # if a closing parenthesis exists, it should be flushed out later as an invalid character

        elif openbracket == -1 and openquote != -1:  # Quotes were found, but not comments
            validaddress, message = ValidateQuotes(address, openquote)
            if validaddress:
                address = message
            else:
                return message

        else:  # Both quotes and comments were found
            if openquote < openbracket:     # The quote was before the parenthesis
                closequote = CloseQuote(address, openquote)
                if closequote == 'invalid':
                    return 'Quotation marks for a quote did not match'
                else:
                    validaddress, message = ValidateQuotes(address, openquote)  # Validates the quote
                    if validaddress:
                        address = message
                    else:
                        return message

            else:   # The parenthesis was before the quote
                closebracket = CloseBracket(address, openbracket)
                if closebracket == 'invalid':
                    return 'Parentheses for a comment did not match'
                else:
                    validaddress, message = ValidateComments(address, openbracket)  # Validates the comment
                    if validaddress:
                        address = message
                    else:
                        return message

# End function


# Function to REPLACE quotes and comments in the address

def ReplaceQuotesComments(address):
    while True:
        openquote, openbracket = OpenQuoteAndBracket(address)  # Assign the opening quote and the opening bracket

        if openquote == -1 and openbracket != -1:  # Comments were found, but not quotes
            closebracket = CloseBracket(address, openbracket)
            address = ReplacePart(address, openbracket, closebracket, 'c')  # Replaces the comment and moves on

        elif openquote == -1 and openbracket == -1:  # Neither quote not comment exists
            return address  # Ends the function

        elif openbracket == -1 and openquote != -1:  # Quotes were found, but not comments
            closequote = CloseQuote(address, openquote)
            address = ReplacePart(address, openquote, closequote, 'q')  # Replaces the quote and move on

        else:  # Both quotes and comments were found
            if openquote < openbracket:  # The quote is first
                closequote = CloseQuote(address, openquote)
                address = ReplacePart(address, openquote, closequote, 'q')  # Replaces the quote
            else:   # The comment is first
                closebracket = CloseBracket(address, openbracket)
                address = ReplacePart(address, openbracket, closebracket, 'c')  # Replaces the comment

# End function


# Function to REMOVE quotes and comments from the address

def RemoveQuotesComments(address):
    while True:
        openquote, openbracket = OpenQuoteAndBracket(address)  # Assign the opening quote and the opening bracket

        if openquote == -1 and openbracket != -1:  # Comments were found, but not quotes
            closebracket = CloseBracket(address, openbracket)
            address = RemoveComment(address, openbracket, closebracket)  # Removes the comment

        elif openquote == -1 and openbracket == -1:  # Neither quote not comment exists
            return address

        elif openbracket == -1 and openquote != -1:  # Quotes were found, but not comments
            closequote = CloseQuote(address, openquote)
            address = ReplacePart(address, openquote, closequote, 'q')  # Quotes are replaced: they always have meaning

        else:  # Both quotes and comments were found
            if openquote < openbracket:
                closequote = CloseQuote(address, openquote)
                address = ReplacePart(address, openquote, closequote, 'q')  # Replace quote
            else:
                closebracket = CloseBracket(address, openbracket)
                address = RemoveComment(address, openbracket, closebracket)  # Remove comment

# End function

# # # # # # # # # # # # # # # # # # # # # # # # # # #
# FUNCTIONS DEALING WITH QUOTES AND COMMENTS END HERE
# # # # # # # # # # # # # # # # # # # # # # # # # # #


# Function confirming there is only one unquoted & uncommented @ sign

def OnlyOneAt(address):
    address = RemoveQuotesComments(address)
    at_num = address.count('@')
    return at_num == 1

# End function


# Function to find and return the position of the uncommented and unquoted @ sign

def FindAt(address):
    address = ReplaceQuotesComments(address)
    at_pos = address.find('@')
    return at_pos

# End function


# Function to validate position of the @ sign

def AtPosValid(address):
    at_pos = FindAt(address)
    return 0 < at_pos < (len(address) - 4)

# End function


# Function for validating dot positioning

def DotsValid(address):
    address = ReplaceQuotesComments(address)    # Quoted or commented dots don't count
    for char in range(len(address)):
        if address[char] == '.':
            if char == 0:
                return 'Address began with a dot'
            elif char == len(address) - 1:
                return 'Address ended with a dot'
            elif address[char + 1] == '.':
                return 'Address contained successive dots'
            elif address[char + 1] == '@':
                return 'Local part ended with a dot'
            elif address[char - 1] == '@':
                return 'Domain began with a dot'
    return 'valid'

# End function


# Function to find and return local part

def FindLocal(address):
    at_pos = FindAt(address)
    localpart = address[:at_pos]
    return localpart

# End function


# Function to find and return domain

def FindDomain(address):
    at_pos = FindAt(address)
    domain = address[at_pos + 1:]
    return domain

# End function


# Function to check if local part is a valid length

def LocalLengthValid(address):
    localpart = FindLocal(address)
    length = len(localpart)
    return 0 < length < 65

# End function


# Function to check for invalid characters in local part

def LocalCharsCorrect(address):
    address = ReplaceQuotesComments(address)
    localpart = FindLocal(address)  # Sets the local part by calling the function, FindLocal()
    restricted = " )\\,:;<>[]\r\n\t"  # Sets a variable with every invalid character
    for char in localpart:
        if not char.isascii() or char in restricted:
            return False
    return True  # If False has not been returned yet, True will now be returned

# End function


# # # # # # # # # # # # # # # # # # # # # #
# IP address validation functions begin here
# # # # # # # # # # # # # # # # # # # # # #

# Function to determine if domain is a literal IP address

def isIP(address):
    domain = FindDomain(RemoveQuotesComments(address))
    return domain[0] == '[' and domain[len(domain) - 1] == ']'

# End Function


# Function to validate an IPv4 address

def IPv4(ip):
    allowed = '.1234567890'  # Allowed characters
    for char in ip:
        if char not in allowed:
            return 'IPv4 address contained ' + char + ', which is invalid'
    if ip[0] == '.':
        return 'IPv4 address began with a dot (".")'
    if ip[len(ip) - 1] == '.':
        return 'IPv4 address ended with a dot (".")'
    labels = ip.split('.')
    if len(labels) < 4:
        return 'IPv4 address contained less than 4 labels'
    if len(labels) > 4:
        return 'IPv4 address contained more than 4 labels'
    for label in labels:
        if label == '':
            return 'Ipv4 address contained successive dots'
        num = int(label)
        if num > 255:
            return 'IPv4 address contained a label with a value of over 255'
    return 'valid'

# End function


# Function  to validate an IPv6 address

def IPv6(ip, form):  # 'form' will be either 'normal' or 'dual'
    if form == 'normal':    # Normal rules:
        if len(ip) == 4:
            return 'The IPv6 label was not proceeded by a colon'
        if ip[4] != ':':
            return 'The IPv6 label was not proceeded by a colon'
        ip = ip[5:]
        if ip == '':
            return 'IPv6 address was empty'
    if ':' not in ip:
        return 'IPv6 address contained no colons'
    allowed = '1234567890ABCDEFabcdef'
    if '.' not in ip:   # No dot in ip indicates normal format: [IPv6:1:1:1:1:1:1:1:1]
        if '::' not in ip:  # "::" is a special IPv6 control character
            if form == 'dual' and ip == ':':  # Allows for the case of [IPv6:::1.1.1.1]
                return 'valid'
            if ip[0] == ':':
                return 'IPv6 address began with a colon'
            if ip[len(ip) - 1] == ':':
                return 'IPv6 address ended with a colon'
            labels = ip.split(':')
            if form == 'dual':  # Normal IPv6 has 8 labels; Dual format has 6 IPv6 + 4 IPv4
                length = 6
            else:
                length = 8
            if len(labels) < length:
                return 'IPv6 address did not contain enough labels'
            if len(labels) > length:
                return 'IPv6 address contained too many labels'
            for label in labels:
                if label == '':
                    return 'IPv6 address contained an empty label'
                if len(label) > 4:
                    return 'IPv6 address contained a label which was too long'
                for char in label:
                    if char not in allowed:
                        return 'IPv6 address contained a label with the invalid character, [', char, ''
            return 'valid'
        else:   # The "::" character accounts for an undefined amount of labels
            labels = ip.split(':')
            if form == 'normal':
                if ip[0] == ':' and ip[1] != ':':
                    return 'IPv6 address began with a colon'
                if ip[len(ip) - 1] == ':' and ip[len(ip) - 2] != ':':
                    return 'IPv6 address ended with a colon'
            if len(labels) > 8:
                return 'IPv6 address contained too many labels'
            double_colon = ip.find('::')
            if '::' in ip[double_colon + 1:]:
                return 'IPv6 address contained more than one double colon, [::]'
            new_ip = ip[:double_colon] + ip[double_colon + 1:]  # Removes the double colon ["::"]
            labels = new_ip.split(':')
            for label in labels:
                if len(label) > 4:
                    return 'IPv6 address contained a label which was too long'
                for char in label:
                    if char not in allowed:
                        return 'IPv6 address contained a label with the invalid character, [', char, ''
            return 'valid'
    lastcolon = -1
    for char in range(len(ip)):
        if ip[char] == ':':
            lastcolon = char    # Finds the last colon
    ipv6 = ip[:lastcolon]   # Dual format
    ipv4 = ip[lastcolon + 1:]   # Dual format
    if IPv4(ipv4) != 'valid':
        return IPv4(ipv4)   # Validates IPv4 part of dual format address
    else:
        if IPv6(ipv6, 'dual') != 'valid':
            return IPv6(ipv6, 'dual')   # Validates IPv6 part of dual format address
        else:
            return 'valid'  # If all is valid, 'valid' is returned

# End function


# Function to completely validate an IP address

def validIP(address):
    domain = FindDomain(address)
    replacedomain = ReplaceQuotesComments(domain)
    start = replacedomain.find('[')
    end = replacedomain.find(']')
    ip = domain[start + 1:end]
    if '(' in ip:
        return 'A comment was found within an ip address'
    if ip[0:4].lower() == 'ipv6':   # Detects if format is IPv6 / ipv6
        ipmode = 6
    else:   # Else format is IPv4
        ipmode = 4
    if ipmode == 4:
        valid = IPv4(ip)
    else:
        valid = IPv6(ip, 'normal')
    return valid

# End function

# # # # # # # # # # # # # # # # # # #
# Functions for IP addresses end here
# # # # # # # # # # # # # # # # # # #


# Function to validate length of domain

def DomainLengthValid(address):
    domain = FindDomain(address)
    return 3 < len(domain) < 254

# End function


# Function checking for a dot in the domain

def DotInDomain(address):
    return '.' in FindDomain(address)

# End function


# Function to find domain labels and check if they are valid lengths

def LabelLengthValid(address):
    domain = FindDomain(address)
    labels = domain.split('.')  # Makes a list of labels
    for label in labels:
        if len(label) < 1 or len(label) > 63:
            return False
    return True

# End function


# Function to check for invalid characters in the domain

def DomainChars(address):
    domain = FindDomain(ReplaceQuotesComments(address))
    allowed = "-.1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"   # All allowed characters
    for char in domain:
        if char not in allowed:
            return char
    return 'valid'

# End function


# Function to check for hyphen invalidity

def HyphensCorrect(address):
    domain = FindDomain(address)  # Find domain from address
    for char in range(len(domain)):
        if domain[char] == '-':
            if char == 0:
                return 'Domain began with a hyphen'
            elif char == len(domain) - 1:
                return 'Domain ended with a hyphen'
            elif domain[char + 1] == '-':
                return 'Domain contained successive hyphens'
            elif domain[char + 1] == '.':
                return 'Domain contained a hyphen followed by a dot'
            elif domain[char - 1] == '.':
                return 'Domain contained a dot followed by a hyphen'
    return 'valid'

# End function


# Function to find the top level domain

def FindTLD(address):
    at_pos = FindAt(address)
    lastdot = at_pos  # Initialises lastdot variable
    for char in range(len(address)):
        if address[char] == '.':
            lastdot = char  # Finds the last dot
    tld = address[lastdot + 1:]  # Sets the Top Level Domain to be everything after the last dot
    return tld  # Returns the Top Level Domain

# End function


# Function to validate the length of the top level domain

def TLD_LengthCorrect(address):
    tld = FindTLD(RemoveQuotesComments(address))
    return len(tld) > 1     # TLD must be at least 2 characters

# End function


# Function to validate characters in the top level domain

def TLD_CharsCorrect(address):
    tld = FindTLD(RemoveQuotesComments(address))  # Finds the Top Level Domain
    allowed = ' 1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    space = False   # Variable indicating whether or not the TLD has white space
    for char in tld:
        if char not in allowed:
            return False
        if char == ' ':
            space = True    # Indicates a white space character has been found
        elif space:
            return False    # Means that a normal character was found after a space (not allowed)
    return True

# End function


# Main validating function

def ValidateEmail(email):
    if LengthInRange(email) == 'valid':
        if AddressContainsAt(email):
            if ValidateQuotesComments(email) == 'valid':
                if OnlyOneAt(email):
                    if AtPosValid(email):
                        if DotsValid(email) == 'valid':
                            if LocalLengthValid(email):
                                if LocalCharsCorrect(email):
                                    if isIP(email):
                                        result = validIP(email)
                                    else:   # These functions below validate a non-IP domain:
                                        if DomainLengthValid(email):
                                            if DotInDomain(email):
                                                if LabelLengthValid(email):
                                                    if DomainChars(email) == 'valid':
                                                        if HyphensCorrect(email) == 'valid':
                                                            if TLD_LengthCorrect(email):
                                                                if TLD_CharsCorrect(email):
                                                                    result = 'valid'
                                                                else:
                                                                    result = 'TLD contained invalid characters'
                                                            else:
                                                                result = 'TLD length was too short'
                                                        else:
                                                            result = HyphensCorrect(email)
                                                    else:
                                                        char = DomainChars(email)
                                                        result = 'Domain contained the invalid character: ' + char
                                                else:
                                                    result = 'The length of a label was invalid'
                                            else:
                                                result = 'Domain did not contain a dot'
                                        else:
                                            result = 'The Domain length was invalid'
                                else:
                                    result = 'Local Part contained invalid characters'
                            else:
                                result = 'The Local Part length was invalid'
                        else:
                            result = DotsValid(email)
                    else:
                        result = "The @ symbol's position was invalid"
                else:
                    result = 'Address contained more than one @ symbol'
            else:
                result = ValidateQuotesComments(email)
        else:
            result = 'Address did not contain an @ symbol'
    else:
        result = LengthInRange(email)
    return result

# End function


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Mainline Starts Here

print('Welcome to the Email Address Validator by Cohen Beveridge')
print('This program can run in "interactive" or "batch" mode')
mode = input('What mode would you like to use? [default is "interactive"] ')
if mode == 'batch':
    print('BATCH mode selected')
    filename = input('What file would you like to be checked? [testfile.txt]\n')
    if filename == '':
        filename = 'testfile.txt'  # The default file
    import os.path  # os.path is imported for checking if the file is real
    if not os.path.isfile(filename):
        print('That file does not exist\n')
    else:
        file = open(filename)  # Opens the file in read mode
        newfilename = 'VALIDATED_' + filename
        while os.path.isfile(newfilename):  # Creates a new file if it exists already, so as not to overwrite it
            newfilename = 'VALIDATED_' + newfilename
        newfile = open(newfilename, 'a')  # Opens the new file for appending
        for aline in file:
            line = aline.strip()  # Strips line of the newline character, as it should not be validated
            outcome = ValidateEmail(line)
            if outcome == 'valid':
                outcome = '*VALID*'
            else:
                outcome = 'INVALID'
            append = outcome + ' -- ' + line + '\n'  # Joins all aspects of the new line
            newfile.write(append)  # Append the line to the new file
        file.close()
        newfile.close()  # Closes both files once finished
        print('Finished validating. A new file called', newfilename, 'has been created')
        print()
else:
    if mode != 'interactive':
        print()
        print('Neither "interactive" nor "batch" was inputted\n')
        print('Defaulting to Interactive mode\n')
    else:
        print('INTERACTIVE mode selected')
    print('At any point, type "end" to end the program')
    print()
    running = True
    while running:
        userinput = input('Enter an Email Address:\n')
        print()
        if userinput == 'end':  # User may enter 'end' to stop the program
            running = False
        else:
            outcome = ValidateEmail(userinput)
            if outcome == 'valid':
                print(userinput, '\nis a VALID Email Address')
            else:
                print(outcome)
                print(userinput, '\nis an INVALID Email Address')
            print()
print('Thank you for using this program')
print('Goodbye')

# End of mainline
