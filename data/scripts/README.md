### Fonte dos dados

Os dados utilizados neste repositório são oriundos do banco de dados do SALIC e portanto é natural que estes dados são gerados por queries `SQL`. Cada dataset é gerado por uma query que está armazenada em arquivos `.sql` na pasta `/data/scripts/`. Portanto para gerar um determinado dataset basta executar sua query.

### Pré-requisitos para baixar datasets e atualizar o ftp

1 - Esteja conectado com a [VPN do SALIC](https://github.com/lappis-unb/salic-ml/wiki/Acesso-via-VPN)

2 - Tenha as seguintes variávies de ambiente com suas credeciais:

```
export DB_HOST=localhost
export DB_PORT=9000
export DB_USER=
export DB_PASSWORD=
export FTP_USER=
export FTP_PASSWORD=
```

### Operações comuns com os datasets

Algumas operações com os datasets são repetitivas, então será descrito como automatizar as operações mais comuns,
### Operações comuns com os datasets

Algumas operações com os datasets são repetitivas, então será descrito abaixo como automatizar as operações mais comuns.

**Baixar datasets a partir de queries sql**

` $ python3 csv_ftp_updater.py path/dir/query1.sql query2.sql --csv_dir=.`

Ao executar executar o comando acima, dois arquivos serão gerados: `query1.csv` e `query2.csv` na pasta `.`. Os parâmetros são caminhos dos arquivos contendo as queries. O parâmetro `csv_dir` estabelece o caminho de uma pasta local onde os arquivos baixados serão salvos.


**Atualizar o ftp a partir de queries sql**

` $ python3 csv_ftp_updater.py path/dir/query1.sql query2.sql --csv_dir=. --update_ftp`

Realiza a mesma opreção acima, além de fazer o upload dos arquivos baixados para o `ftp`.

**Fazer upload de .csv para o ftp**

` $ python3 csv_ftp_updater.py query.csv --upload_csv`

### Documentação do script utilizado

O script `csv_ftp_updater.py` se encontra na pasta `/data/scripts/`. Para ver sua documentação, digite:

` $ python3 csv_ftp_updater.py -h`
