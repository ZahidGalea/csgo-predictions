import io
import os
import shutil

from google.cloud import bigquery
from google.cloud.bigquery.job import WriteDisposition


def get_all_json_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory)]


def ensure_table_structure(client, dataset_name, table_name):
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)

    # Definir el esquema deseado
    schema = [
        bigquery.SchemaField("json_content", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("file_name", "STRING", mode="REQUIRED"),
    ]

    try:
        table = client.get_table(table_ref)
        # Aquí puedes añadir lógica para verificar y/o actualizar el esquema si es necesario
    except Exception as e:
        # Si la tabla no existe, la creamos
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"Table {table_name} created.")


def upload_to_bigquery(data_str, dataset_name, table_name):
    client = bigquery.Client()
    table_ref = client.dataset(dataset_name).table(table_name)

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = "|"  # un delimitador improbable
    job_config.skip_leading_rows = 0
    job_config.autodetect = True
    if "matches" in data_str:
        job_config.write_disposition = WriteDisposition.WRITE_APPEND
    else:
        job_config.write_disposition = WriteDisposition.WRITE_TRUNCATE

    csv_buffer = io.StringIO()

    with open(data_str, "r") as f:
        for line in f:
            escaped_line = line.strip()  # escapamos comillas dobles
            csv_entry = f'{escaped_line}|{os.path.basename(data_str)}\n'
            csv_buffer.write(csv_entry)

    # Retrocedemos al inicio del buffer
    csv_buffer.seek(0)

    load_job = client.load_table_from_file(
        csv_buffer, destination=table_ref, job_config=job_config
    )
    load_job.result()


def move_to_processed(directory, file):
    ruta_origen = file
    ruta_destino = f"data/processed/{directory}/{file.split('/')[-1]}"
    shutil.move(ruta_origen, ruta_destino)


if __name__ == "__main__":
    folders = ["events", "best_players", "best_teams", "matches","events_ongoing"]
    for directory in folders:
        TABLE_NAME = directory
        DIRECTORY = f"data/{directory}"

        DATASET_NAME = "raw"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credential.json"
        json_files = get_all_json_files(DIRECTORY)
        for json_file in json_files:
            try:
                print("Uploading file ", json_file)
                upload_to_bigquery(json_file, DATASET_NAME, TABLE_NAME)
                # move_to_processed(directory=directory, file=json_file)
            except Exception as e:
                print(e)
                print(f"Failed to upload {json_file}")
