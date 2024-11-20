from faker import Faker
import random

faker = Faker("pt_BR")
nomes_departamentos = ["Ciência da Computação", "Engenharia Civil", "Administração"]

def montarID(qtIds, qtDigitos):
    Array = []
    for _ in range(qtIds):
        novoid = random.randint(10**(qtDigitos - 1), 10**qtDigitos - 1)
        while novoid in Array:
            novoid = random.randint(10**(qtDigitos - 1), 10**qtDigitos - 1)
        Array.append(str(novoid))  
    return Array


def criarnome():
    return f"{faker.unique.first_name()} {faker.unique.last_name()}"

qtalunos = 50
qtprof = 6
qttcc = 3
integrantestcc = 2

aluno_id = montarID(qtalunos, 8)
prof_id = montarID(qtprof, 7)
curso_id = montarID(3, 6)
tcc_id = montarID(qttcc, 5)
dept_id = montarID(3, 4)
disc_id = montarID(6, 3)


class Aluno:
    def __init__(self, aluno_id, curso_id, aulas, grupo_tcc=None, tcc=None, formado=False):
        self.aluno_id = aluno_id
        self.nome = criarnome()
        self.curso_id = curso_id
        self.aulas = aulas 
        self.grupo_tcc = grupo_tcc or 'NDA'
        self.tcc = tcc or 'NDA'
        self.formado = formado

    def insert_dados(self):
        return f"INSERT INTO aluno (aluno_id, nome, curso_id) VALUES ('{self.aluno_id}', '{self.nome}', '{self.curso_id}');\n"

    def insert_historico(self):
        comandos = []
        for aula in self.aulas:
            comandos.append(
                f"INSERT INTO historico_aluno (aluno_id, disc_id, curso_id, ano, semestre, nota, grupo_tcc, tcc) "
                f"VALUES ('{self.aluno_id}', '{aula.disc_id}', '{self.curso_id}', {aula.ano}, {aula.semestre}, {aula.nota}, '{self.grupo_tcc}', '{self.tcc}');\n"
            )
        return "".join(comandos)
    
    def insert_alunos_com_grupo_tcc(self):
        if self.grupo_tcc != 'NDA':
            return f"INSERT INTO alunos_com_grupo_tcc (aluno_id, nome, curso_id, grupo_tcc) VALUES ('{self.aluno_id}', '{self.nome}', '{self.curso_id}', '{self.grupo_tcc}');\n"
        return ""
    
    def insert_formado(self):
        if self.formado:
            return f"INSERT INTO formados (aluno_id, nome) VALUES ('{self.aluno_id}', '{self.nome}');\n"
        return ""

class Professor:
    def __init__(self, prof_id, dept_id, aula, chefe=False):
        self.prof_id = prof_id
        self.nome = criarnome()
        self.aula = aula
        self.departamento = dept_id if chefe else 'NDA'

    def insert_dados(self):
        return f"INSERT INTO professor (prof_id, nome) VALUES ('{self.prof_id}', '{self.nome}');\n"

    def insert_historico(self):
        return (
            f"INSERT INTO historico_professor (prof_id, disc_id, semestre, ano, departamento) "
            f"VALUES ('{self.prof_id}', '{self.aula.disc_id}', {self.aula.semestre}, {self.aula.ano}, '{self.departamento}');\n"
        )

class Aula:
    def __init__(self, disc_id, semestre, ano):
        self.disc_id = disc_id
        self.semestre = semestre
        self.ano = ano
        self.nota = random.uniform(5, 10)  

class Departamento:
    def __init__(self, dept_id, nome, chefe_prof_id, chefe_nome):
        self.dept_id = dept_id
        self.nome = nome
        self.chefe_prof_id = chefe_prof_id
        self.chefe_nome = chefe_nome

    def insert_dados(self):
        return (
            f"INSERT INTO departamento (dept_id, nome, chefe_prof_id, chefe_nome) "
            f"VALUES ('{self.dept_id}', '{self.nome}', '{self.chefe_prof_id}', '{self.chefe_nome}');\n"
        )


class TCC:
    def __init__(self, tcc_id, tcc_nome, prof_id, curso_id, integrantes):
        self.tcc_id = tcc_id
        self.tcc_nome = tcc_nome
        self.prof_id = prof_id
        self.curso_id = curso_id
        self.integrantes = integrantes

    def insert_dados(self):
        return f"INSERT INTO tcc (tcc_id, nome, curso_id, prof_id) VALUES ('{self.tcc_id}', '{self.tcc_nome}', '{self.curso_id}', '{self.prof_id}');\n"

    def insert_grupo_tcc(self):
        comandos = []
        for integrante in self.integrantes:
            comandos.append(
                f"INSERT INTO grupo_tcc (tcc_id, aluno_id) VALUES ('{self.tcc_id}', '{integrante}');\n"
            )
        return "".join(comandos)


aulas = [Aula(disc_id[i], random.randint(1, 2), random.randint(2015, 2024)) for i in range(len(disc_id))]
alunos = []
for i in range(qtalunos):
    grupo_tcc = None
    tcc = None
    formado = random.choice([True, False]) 
    
    if i < qttcc * integrantestcc:
        grupo_tcc = tcc_id[i // integrantestcc]
        tcc = f"TCC {i // integrantestcc + 1}"
    
    aluno = Aluno(aluno_id[i], curso_id[i % len(curso_id)], aulas[:2] if i % 2 == 0 else [aulas[0]], grupo_tcc, tcc, formado)
    alunos.append(aluno)

profs = [Professor(prof_id[i], dept_id[i % len(dept_id)], aulas[i % len(aulas)], chefe=(i < 3)) for i in range(qtprof)]
tccs = [TCC(tcc_id[i], f"TCC {i+1}", prof_id[i], curso_id[i % len(curso_id)], [aluno_id[i], aluno_id[i+1]]) for i in range(qttcc)]

departamentos = []
for i, nome in enumerate(nomes_departamentos):
    if i < len(profs) and profs[i].departamento != 'NDA': 
        departamentos.append(
            Departamento(dept_id[i], nome, profs[i].prof_id, profs[i].nome)
        )


with open("dadosCassandra.cql", "w", encoding="utf-8") as arquivo:
    for aluno in alunos:
        arquivo.write(aluno.insert_dados())
        arquivo.write(aluno.insert_historico())
        arquivo.write(aluno.insert_alunos_com_grupo_tcc())
        if aluno.formado:
            arquivo.write(aluno.insert_formado())

    for prof in profs:
        arquivo.write(prof.insert_dados())
        arquivo.write(prof.insert_historico())

    for tcc in tccs:
        arquivo.write(tcc.insert_dados())
        arquivo.write(tcc.insert_grupo_tcc())
    
    for dept in departamentos:
        arquivo.write(dept.insert_dados())
