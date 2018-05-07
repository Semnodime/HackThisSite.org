"""
Level 2
This level is about image analyzing.

The pixels in ./PNG.png are numbered 0..99 for the first row, 100..199 for the second row etc.
White pixels represent ascii codes.
The ascii code for a particular white pixel is equal to the offset from the last white pixel.
For example, the first white pixel at location 65 would represent ascii code 65 ('A'),
the next at location 131 would represent ascii code (131 - 65) = 66 ('B') and so on.

The text contained in the image is the answer encoded in Morse, where "a test" would be encoded as ".- / - . ... -"
"""

import PIL.Image


def png_to_ascii(path):
    """ Read the png where each distance between white pixels will be encoded into an ASCII character """
    image = PIL.Image.open(path)
    rgb_data = image.convert('RGB').getdata()
    ascii_result = ''
    counter = 0
    for pixel in rgb_data:
        is_white = pixel == (255, 255, 255)
        if is_white:
            ascii_char = chr(counter)
            ascii_result += ascii_char
            # print('White pixel with distance %dpx (%r) since last white pixel.' % (counter, ascii_char))
            counter = 0
        counter += 1

    return ascii_result


def decode_morse(morse_code, mode='international_morse', ignore_err=True):
    """
    Decodes morse into clear text based on specifications by wikipedia
    https://en.wikipedia.org/wiki/File:Morse_comparison.svg
    """
    continental_gerke = {
        '.-': 'A',
        '.-.-': 'Ä',
        '-...': 'B',
        '-.-.': 'C',
        '----': 'CH',
        '-..': 'D',
        '.': 'E',
        '..-.': 'F',
        '--.': 'G',
        '....': 'H',
        '..': 'I',
        '.---': 'J',
        '-.-': 'K',
        '.-..': 'L',
        '--': 'M',
        '-.': 'N',
        '.-...': 'O',
        '---.': 'Ö',
        '.....': 'P',
        '--.-': 'Q',
        '.-.': 'R',
        '...': 'S',
        '-': 'T',
        '..-': 'U',
        '..--': 'Ü',
        '...-': 'V',
        '.--': 'W',
        '..-...': 'X',
        '--...': 'Y',
        '.--..': 'Z',
        '.--.': '1',
        '..-..': '2',
        '...-.': '3',
        '....-': '4',
        '---': '5',
        '......': '6',
        '--..': '7',
        '-....': '8',
        '-..-': '9',
        '______': '0',  # full-6-dot representation can vary
    }

    international_morse = {
        '.-': 'A',
        '-...': 'B',
        '-.-.': 'C',
        '-..': 'D',
        '.': 'E',
        '..-.': 'F',
        '--.': 'G',
        '....': 'H',
        '..': 'I',
        '.---': 'J',
        '-.-': 'K',
        '.-..': 'L',
        '--': 'M',
        '-.': 'N',
        '---': 'O',
        '.--.': 'P',
        '--.-': 'Q',
        '.-.': 'R',
        '...': 'S',
        '-': 'T',
        '..-': 'U',
        '...-': 'V',
        '.--': 'W',
        '-..-': 'X',
        '-.--': 'Y',
        '--..': 'Z',
        '-----': '0',
        '.----': '1',
        '..---': '2',
        '...--': '3',
        '....-': '4',
        '.....': '5',
        '-....': '6',
        '--...': '7',
        '---..': '8',
        '----.': '9',
    }

    extensions = {
        '/': ' ',
        '...---...': 'SOS',
        '.-...': '&',
        '--..--': ',',
        '..--..': '?',
        '-.-.--': '!',
        '-...-': '=',
        '.-.-.-': '.',
        '.----.': "'",
        '.-..-.': '"',
        '-.-.-.': ';',
        '-....-': '-',
        '..--.-': '_',
        '-.--.': '(',
        '-.--.-': ')',
        '-..-.': '/',
        '.-.-.': '+',
        '---...': ':',
        '.--.-.': '@',
        '...-..-': '$',
    }
    decoders = {
        'continental_gerke': continental_gerke,
        'international_morse': international_morse,
    }
    decoder = decoders.get(mode)
    if not decoder:
        raise ValueError('The specified morse version is not supported', mode)

    clean_morse_code = morse_code.strip(' ').replace('  ', ' ').replace('/', ' / ').split(' ')
    print('Attempting to decode %r in mode %r' % (clean_morse_code, mode))
    for item in clean_morse_code:
        if not item:
            continue
        decoded_item = decoder.get(item) or extensions.get(item)
        if not decoded_item:
            print('Could not decode morse %r' % item)
            if ignore_err:
                continue

        yield decoded_item


if __name__ == '__main__':
    print('This analyser converts ./PNG.png into ascii values then morse and finally cleartext words')

    ascii_str = png_to_ascii('PNG.png')
    print('Decoded image white pixel distance into the following ascii: %r' % ascii_str)

    # As the code '----' is not defined in ITU morse I had to implement and try gerke variant
    # answer = ''.join(decode_morse(ascii_str, mode='continental_gerke', ignore_err=False))

    # But codes like '..---' and '---..' clearly indicate ITU morse
    # Probably its invalid...? I'll try ignoring decoding errors.
    # answer = ''.join(decode_morse(ascii_str, mode='international_morse', ignore_err=True))

    # Turns out I missed that pixel distances include white pixels in the calculation.
    # Now decoding the result with ITU morse works as well
    answer = ''.join(decode_morse(ascii_str, mode='international_morse', ignore_err=False))

    print('Decoded morse code into the following answer: %r' % answer)
