import math
from criptolib.utils.validacao import Validar
from criptolib.math.modular import InteiroModular


class Congruencias:
    def __init__(self, residuos: list[int], modulos: list[int]):
        Validar.inteiros(*residuos)
        Validar.modulo(*modulos)
        Validar.coprimos_2_a_2(modulos)
        
        if not residuos or not modulos:
            raise ValueError("As listas de resíduos e módulos não podem ser vazias.")
        if len(residuos) != len(modulos):
            raise ValueError("O tamanho do vetor de resíduos deve ser igual ao do vetor de módulos.")

        self.residuos = residuos
        self.modulos = modulos

    def resolver(self) -> int:
        m = math.prod(self.modulos)
        m_i = [m // modulo for modulo in self.modulos]
        m_i_inv = [InteiroModular(m_i_aux, modulo).inverso_modular().valor for m_i_aux, modulo in zip(m_i, self.modulos)]

        resposta = sum(residuo * m_i_aux * m_i_inv_aux for residuo, m_i_aux, m_i_inv_aux in zip(self.residuos, m_i, m_i_inv))
        return resposta % m
