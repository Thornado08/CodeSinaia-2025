def number_to_words(n):
    if not isinstance(n, int):
        return None
    if n < 0 or n >= 4000:
        return "Number out of range (0 to 3999)"
    
    if n == 0:
        return "zero"
    
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
             "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty",
            "seventy", "eighty", "ninety"]

    def convert_hundreds(num):
        result = ""
        if num >= 100:
            result += ones[num // 100] + " hundred"
            num %= 100
            if num > 0:
                result += " "
        if 10 <= num < 20:
            result += teens[num - 10]
        else:
            if num >= 20:
                result += tens[num // 10]
                if num % 10 > 0:
                    result += "-" + ones[num % 10]
            elif num > 0:
                result += ones[num]
        return result

    parts = []

    if n >= 1000:
        parts.append(ones[n // 1000] + " thousand")
        n %= 1000
        if n > 0:
            parts.append(convert_hundreds(n))
    else:
        parts.append(convert_hundreds(n))

    return " ".join(parts)
