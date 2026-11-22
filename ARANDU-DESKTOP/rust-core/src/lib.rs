//! ARANDU Desktop — estado mínimo do protótipo, sem I/O nem coleta de eventos.
//! Experimentos de Seed/ECA devem continuar em outros processos e repositórios.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Rio {
    Memoria,
    Abertos,
    Frequentes,
}

#[derive(Debug, Default, PartialEq, Eq)]
pub struct Navegacao {
    rio: Option<Rio>,
    aberta: bool,
}

impl Navegacao {
    pub fn selecionar(&mut self, rio: Rio) {
        self.rio = Some(rio);
        self.aberta = true;
    }

    pub fn recolher(&mut self) {
        self.rio = None;
        self.aberta = false;
    }

    pub fn rio(&self) -> Option<Rio> {
        self.rio
    }

    pub fn aberta(&self) -> bool {
        self.aberta
    }
}

/// Contrato seguro: nenhuma conexão ECA é ativada por padrão.
#[derive(Debug, Default)]
pub struct PonteEca {
    autorizada: bool,
}

impl PonteEca {
    pub fn autorizada(&self) -> bool {
        self.autorizada
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tres_rios_sao_reversiveis() {
        let mut n = Navegacao::default();
        for rio in [Rio::Memoria, Rio::Abertos, Rio::Frequentes] {
            n.selecionar(rio);
            assert_eq!(n.rio(), Some(rio));
            assert!(n.aberta());
            n.recolher();
            assert_eq!(n.rio(), None);
            assert!(!n.aberta());
        }
    }

    #[test]
    fn eca_nunca_conecta_sem_autorizacao_explicita() {
        assert!(!PonteEca::default().autorizada());
    }
}
