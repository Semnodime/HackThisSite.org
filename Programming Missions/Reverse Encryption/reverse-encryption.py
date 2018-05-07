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


def md5(data):
    data = str(data).encode()
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def eval_cross_total(str_md5):
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


def encrypt_string(str_string, str_password):
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
        arr_encrypted_values.append(str(ord(str_string[i]) + int(str_password_md5[i % 32], 16) - int_md5_total))
        int_md5_total = eval_cross_total((md5(str_string[:i + 1]))[:16] + md5(int_md5_total)[:16])
    return ' '.join(arr_encrypted_values)


if __name__ == '__main__':
    print('This program attempts to output the last serial of ./serials.txt which got obfuscated by ./crypter.php')
    # print('A test of the transcribed php5.x.x to python [WORKS]:', encrypt_string('somestring', 'somepassword'))
    # -81 -111 -125 -171 -136 -104 -84 -123 -146 -123
