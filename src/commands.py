from enum import StrEnum


class Commands(StrEnum):
    NOTE_LA = "a"
    NOTE_SI = "b"
    NOTE_DO = "c"
    NOTE_RE = "d"
    NOTE_MI = "e"
    NOTE_FA = "f"
    NOTE_SOL = "g"
    RANDOM_NOTE = "?"

    REPEAT_NOTE_OR_CELL_RING_TONE_CHAR_1 = "i"
    REPEAT_NOTE_OR_CELL_RING_TONE_CHAR_2 = "o"
    REPEAT_NOTE_OR_CELL_RING_TONE_CHAR_3 = "u"

    INC_VOLUME_1_OCTAVE = "r+"
    DEC_VOLUME_1_OCTAVE = "r-"
    INC_BPM_80_UNITS = "bpm+"
    RANDOM_BPM = ";"

    SILENCE = " "
    CHANGE_INSTRUMENT = "\n"
    DOUBLE_VOLUME = "+"
    RESET_VOLUME = "-"

    @staticmethod
    def explanation() -> str:
        return """
            Letra A ou a: Nota Lá                   
            Letra B ou b: Nota Si                   
            Letra C ou c: Nota Dó                   
            Letra D ou d: Nota Ré                   
            Letra E ou e: Nota Mi                   
            Letra F ou f: Nota Fá                   
            Letra G ou g: Nota Sol                  
            Caractere Espaço: Silêncio ou pausa
            Caractere + (sinal de adição): Dobra o volume
            Caractere - (sinal de subtração): Restaura o volume para o padrão
            Letras I ou i, O ou o, U ou u: Se caractere anterior era NOTA (A a G), repete nota; Caso contrário, faz som de “Telefone tocando”
            Letra R ou r seguida de sinal de adição: Aumenta volume em uma oitava
            Letra R ou r seguida de sinal de subtração: Diminui volume em uma oitava
            Ponto de interrogação (?): Toca uma nota aleatória (de A a G)
            Caractere NL (nova linha): Troca instrumento
            Letras BPM seguidas de sinal de adição: Aumenta BPM em 80 unidades 
            Ponto e vírgula (;): Atribui um BPM aleatório
            
            Outros caracteres: o caractere será ignorado, e o programa continuará a execução.
        """  # noqa: E501

    @classmethod
    def notes(cls) -> list["Commands"]:
        return [
            cls.NOTE_LA,
            cls.NOTE_SI,
            cls.NOTE_DO,
            cls.NOTE_RE,
            cls.NOTE_MI,
            cls.NOTE_FA,
            cls.NOTE_SOL,
            cls.RANDOM_NOTE,
        ]

    @classmethod
    def repeat_commands(cls) -> list["Commands"]:
        return [
            cls.REPEAT_NOTE_OR_CELL_RING_TONE_CHAR_1,
            cls.REPEAT_NOTE_OR_CELL_RING_TONE_CHAR_2,
            cls.REPEAT_NOTE_OR_CELL_RING_TONE_CHAR_3,
        ]

    @classmethod
    def mandatory(cls) -> list["Commands"]:
        """List commands where AT LEAST one of them must be present in the input."""

        return cls.notes() + cls.repeat_commands()
