"""
Level 3
This level is about reversing an encryption algorithm.

The original text is a bunch of fake serial numbers.
Look into ./serials_example.txt to see some examples of what they look like.
The PHP-code which is used for the encryption is given in ./crypter.php:

This is a example of the encrypted text:
(Ignore newlines and ''' delimiters)
'''
-192 -216 -187 -174 -163 -147 -190 -203 -110 -173 -170 -208 -148 -185 -187 -172 -174 -225 -181 -265 -134 -170 -160 -156
-158 -146 -146 -189 -131 -125 -147 -170 -158 -139 -139 -193 -180 -181 -185 -225 -176 -176 -146 -149 -197 -55 -214 -115
-154 -209 -118 -170 -172 -135 -204 -165 -158 -154 -188 -239 -147 -186 -111 -192 -154 -126 -130 -194 -127 -184 -191 -145
-232 -146 -201 -189 -175 -192 -182 -196 -145 -150 -160 -150 -182 -169 -187 -188 -182 -118 -166 -189 -74 -93 -191 -178
-209 -200 -153 -241
'''

The last one of the serial numbers you decrypted is the answer.
"""
import hashlib
import itertools


def md5(data):
    data = str(data).encode()
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def eval_cross_total(str_md5: str):
    """
    Reimplementation of php equivalent:
    //------------------------------------------------------------------------------------
    function evalCrossTotal($strMD5)
    {
        $intTotal = 0;
        $arrMD5Chars = str_split($strMD5, 1);
        foreach ($arrMD5Chars as $value)
        {
            $intTotal += '0x0'.$value;
        }
        return $intTotal;
    }//-----------------------------------------------------------------------------------
    """
    int_total = 0
    for hex_char in str_md5:
        int_total += int(hex_char, 16)
    return int_total


def encrypt_string(str_string: str, str_password: str):
    """
    Reimplementation of php equivalent:
    //------------------------------------------------------------------------------------
    function encryptString($strString, $strPassword)
    {
        // $strString is the content of the entire file with serials
        $strPasswordMD5 = md5($strPassword);
        $intMD5Total = evalCrossTotal($strPasswordMD5);
        $arrEncryptedValues = array();
        $intStrlen = strlen($strString);
        for ($i=0; $i<$intStrlen; $i++)
        {
            $arrEncryptedValues[] =  ord(substr($strString, $i, 1))
                +  ('0x0' . substr($strPasswordMD5, $i%32, 1))
                -  $intMD5Total;
            $intMD5Total = evalCrossTotal(substr(md5(substr($strString,0,$i+1)), 0, 16)
                .  substr(md5($intMD5Total), 0, 16));
        }
        return implode(' ' , $arrEncryptedValues);
    }//-----------------------------------------------------------------------------------
    """
    str_password_md5 = md5(str_password)
    int_md5_total = eval_cross_total(str_password_md5)
    arr_encrypted_values = []
    for i in range(len(str_string)):
        ascii_val = ord(str_string[i])
        pw_partial = int(str_password_md5[i % 32], 16)
        arr_encrypted_values.append(str(ascii_val + pw_partial - int_md5_total))
        int_md5_total = eval_cross_total((md5(str_string[:i + 1]))[:16]) + eval_cross_total(md5(int_md5_total)[:16])
    return ' '.join(arr_encrypted_values)


def serials_mask():
    """ My assumption of what the serials will always look like """
    return 'xxx-xxx-OEM-xxx-1.1Nxxx-xxx-OEM-' \
           'xxx-1.1Nxxx-xxx-OEM-xxx-1.1Nxxx-' \
           'xxx-OEM-xxx-1.1Nxxx-xxx-OEM-xxx-' \
           '1.1N'


def serial_gen(prefix_data='', length=None):
    """ Generates a string of valid serial data based on prefix and combinations for the places left """
    small_space = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    s = small_space
    base = [s, s, s, '-', s, s, s, '-', 'O', 'E', 'M', '-', s, s, s, '-', '1', '.', '1', '\n']

    # Automatically set length to generate a serial snipped one char longer than the given prefix
    if not length:
        length = len(prefix_data) + 1

    # Make it possible to generate longer snippets than one serial key in row by recursive use of itertools
    if length > len(base):
        prefix_data_low = prefix_data[:len(base)]
        prefix_data_high = prefix_data[len(base):]

        for serial_low, serial_high in itertools.product(serial_gen(prefix_data=prefix_data_low, length=len(base)),
                                                         serial_gen(prefix_data=prefix_data_high,
                                                                    length=length - len(base))):
            yield (serial_low + serial_high)
    else:
        # Only one serial needs to be generated
        for pos in range(len(base)):
            if pos < len(prefix_data):
                base[pos] = prefix_data[pos]

        if length == 1:
            # Recursion anchor
            for serial in base[length - 1]:
                yield serial
        else:
            # Dynamic length of the generator output is achieved by recursion and itertools as well
            for serial_low, serial_high in itertools.product(serial_gen(prefix_data=prefix_data, length=length - 1),
                                                             base[length - 1]):
                yield (serial_low + serial_high)


best_length = 0


def deobfuscate(obfuscated_serials: str):
    """ Recursive deobfuscation based on itertools"""
    encrypted_values = [int(x) for x in obfuscated_serials.split(' ')]
    print('Attempting to deobfuscate %d values:' % len(encrypted_values), encrypted_values)

    def bruteforce_next_char(int_md5_total, prefix_data=''):
        # Loop through all possible serial keys but increase length of serial snippet only on success to increase speed
        for data in serial_gen(prefix_data=prefix_data):
            i = len(prefix_data)
            ascii_val = ord(data[i])

            # progress forward if working condition (extracted from the obfuscator) is satisfied
            # assume encrypted_values[i] <===> ascii_val + pw_partial - int_md5_total:
            pw_partial = encrypted_values[i] - ascii_val + int_md5_total
            if pw_partial not in range(16):
                # print('partial failed for', i, data, pw_partial, int_md5_total)
                continue

            global best_length
            if i > best_length:
                best_length = i
                print(repr(data))

            if i + 1 < len(encrypted_values):
                next_int_md5_total = eval_cross_total((md5(data[:i + 1]))[:16]) + eval_cross_total(
                    md5(int_md5_total)[:16])
                bruteforce_next_char(prefix_data=data, int_md5_total=next_int_md5_total)
            else:
                print('End of obfuscated data, possible deobfuscation:', repr(data))

    for int_md5_total in range(eval_cross_total('f' * len(md5('')))):
        bruteforce_next_char(prefix_data='', int_md5_total=int_md5_total)


if __name__ == '__main__':
    print('This program attempts to output the last serial of ./serials.txt which got obfuscated by ./crypter.php')

    # print('A test of the transcribed php5.x.x to python [WORKS]:', encrypt_string('somestring', 'somepassword'))
    # -81 -111 -125 -171 -136 -104 -84 -123 -146 -123

    # Generate some sample obfuscated data to test deobfuscation
    # with open('serials_example.txt') as f:
    #     serials_example_file = f.read()
    # obfuscated = encrypt_string(serials_example_file, 'some_password')
    # print(obfuscated)
    # deobfuscate(obfuscated)

    # Load data from serials file which contains the obfuscated data provided by the challenge
    with open('serials.txt') as f:
        serials_file = f.read()
    deobfuscate(serials_file)
