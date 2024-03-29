import numpy as np
from PIL import Image


def main():

    def Encode(src, message, dest):

        img = Image.open(src, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        total_pixels = array.size // n

        message += "$t3g0"
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)

        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")

        else:
            index = 0
            for p in range(total_pixels):
                for q in range(0, 3):
                    if index < req_pixels:
                        array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                        index += 1

            array = array.reshape(height, width, n)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            enc_img.save(dest)
            print("Image Codificada com Sucesso")

    # decoding function
    def Decode(src):

        img = Image.open(src, 'r')
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        total_pixels = array.size // n

        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(0, 3):
                hidden_bits += (bin(array[p][q])[2:][-1])

        hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

        message = ""
        for i in range(len(hidden_bits)):
            if message[-5:] == "$t3g0":
                break
            else:
                message += chr(int(hidden_bits[i], 2))
        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
        else:
            print("No Hidden Message Found")

    # main function
    def Stego():
        print("--Bem Vindo ao 3$t3g0--")

        print("1: Codificar")
        print("2: Decodificar")

        func = input()

        if func == '1':
            print("Digite o Nome da imagem fonte:")
            src = input()
            print("Digite a Mensagem Secreta:")
            message = input()
            print("Digite o Nome da Imagem Codificada:")
            dest = input()
            print("Codificando...")
            Encode(src, message, dest)

        elif func == '2':
            print("Digite o Nome da Imagem Codificada:")
            src = input()
            print("Decodificando...")
            Decode(src)

        else:
            print("ERRO: Opção inválida")

    Stego()

if __name__ == '__main__':
    main()