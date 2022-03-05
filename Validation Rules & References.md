Validation Rules

These are the validation rules which my program follows. These rules were created with careful research.


1.	Total length must be between 6 and 255 characters
2.	Address must contain an ‘@’ sign
3.	Quoting can be done by enclosing a label in double quotes (")
4.	Escaping may be done with a backslash before the character; an escaped backslash does not escape anything else
5.	Quotation marks must match unless escaped
6.	A quote may either occupy the entire local part, or occupy an entire label, separated by dots, inside the local part
7.	An @ sign must occur somewhere after the rightmost quote
8.	Quoted labels can include all characters, except for Tab, CR, LF, [, ] unless escaped
9.	Comments are indicated with parentheses
10.	Comments may be within comments, but any opening '(' must have a ')' to match
11.	Comments can occur at the start/end of labels or parts
12.	Characters within comment must follow the same rules as quoted labels, but square brackets are allowed
13.	There must be only one unquoted and uncommented ‘@’ sign
14.	The @ sign must have something before it and at least 4 characters after it
15.	Both the local part and the domain must not begin with a dot, end with a dot, or contain successive dots unless quoted/commented
16.	The local part must be between 1 and 64 characters
17.	The local part must not contain these characters: ) \ , : ; < > [ ] Tab CR LF unless they are quoted/commented
18.	The domain must be a maximum of 253 characters, minimum of 4
19.	The domain must contain at least one dot
20.	Labels (dot separated strings) must be 63 or less characters
21.	The domain must contain only alphabetical characters, digits, dots, and hyphens
22.	Labels in the domain must not begin with a hyphen, end with a hyphen, or contain successive hyphens
23.	Top level domain (everything after rightmost dot) must be more than one character
24.	The Top level domain must only have alphabetical and/or numerical characters
25.	Domain can be an ip address enclosed by square brackets “[“, ”]”: either IPv4 or IPv6
26.	Comments my occur before or after the square brackets, but not within the brackets
27.	IPv4 is 4 integers separated by dots
28.	The IPv4 integers must be under 256
29.	IPv6 (indicated with “IPv6:”) can be normal format or dual format
30.	Normal format is 8 hexadecimal values with 1 – 4 characters
31.	Hexadecimal values may have the letters a – f, and digits
32.	Dual IPv6 format is 6 hexadecimal values separated by colons “:”, followed by an IPv4 address
33.	IPv6 can contain “::” once, representing insignificant zeros (allowing for an undetermined number of parts less than 8/6)



References:

Akins, T. (n.d.). Email Validation Done Right. http://rumkin.com/software/email/
Clarke, B. (2021). eMail Validator Activity Outline. eMail Validator Activity Outline.pdf
Comparing E-mail Address Validating Regular Expressions (2012). CN Blogs. https://www.cnblogs.com/hyqing/p/3421730.html
Fuentes, E. (2019). IP address vs domain in an email address. https://www.serviceobjects.com/blog/ip-address-vs-domain-in-an-email-address/
Haack, P. (2007). I Knew How To Validate An Email Address Until I Read The RFC. http://haacked.com/archive/2007/08/21/i-knew-how-to-validate-an-email-address-until-i.aspx/
Henderson, C. (n.d.). RFC 822 Email Address Parser in PHP. https://code.iamcal.com/php/rfc822/
Hinden, R. (2006). RFC 4291 - IP Version 6 Addressing Architecture. https://datatracker.ietf.org/doc/html/rfc4291
JavaScript form validation - checking email (n.d.). W3 resources. https://www.w3resource.com/javascript/form/example-javascript-form-validation-email-REC-2822.html
Klensin, J. (2004). RFC 3696 - Application Techniques for Checking and Transformation of Names. https://datatracker.ietf.org/doc/html/rfc3696
Nagar, R. (n.d.). JMail Email Address Validation. https://www.rohannagar.com/jmail/
Resnick, P. (2008). RFC 5322 - Internet Message Format. https://datatracker.ietf.org/doc/html/rfc5322
Wikipedia. (2021). Email address. https://en.wikipedia.org/wiki/Email_address
