import os

import numpy as np
import ollama

from .models import TransportationData


def generate_embedding(text: str) -> np.ndarray:
  """
  Generate embedding vectors using ollama/llama3.2 model.

  Args:
      text (str): Input text to generate embeddings for

  Returns:
      np.ndarray: A squeezed numpy array containing the embedding vectors

  Raises:
      ValueError: If input text is empty or not a string
      RuntimeError: If embedding generation fails
  """
  if not isinstance(text, str) or not text.strip():
    raise ValueError("Input text must be a non-empty string")

  try:
    response = ollama.embed(
        model="llama3.2",
        input=text
    )

    return np.array(response["embeddings"]).squeeze()

  except Exception as e:
    raise RuntimeError(f"Failed to generate embedding: {str(e)}")


def parse_and_store_md():
  """
  Parse testinfo.md file and store data into database

  This function:
  1. Reads a markdown file containing transportation data in table format
  2. Parses each valid row of the table
  3. Converts text data into TransportationData objects
  4. Generates embeddings for text descriptions
  5. Bulk saves all data to database after clearing existing records
  """
  # Get full path to the markdown file
  filepath = os.path.join(os.path.dirname(__file__), '../testinfo.md')
  # Read all lines from file
  with open(filepath, 'r', encoding='utf-8') as file:
    lines = file.readlines()

  data_rows = []
  for line in lines:
    # Only process lines that are part of the table (contain | separator)
    if line.strip() and "|" in line:
      columns = line.split('|')  # Split line into columns

      # Skip header rows and separator lines by checking:
      # 1. If there are enough columns
      # 2. If it's a header row containing "行政區"
      # 3. If it's a separator row containing only "-" or empty strings
      if (
          len(columns) < 10
          or "行政區" in columns[1]
          or all(col == "-" or col == "" for col in columns[1])
      ):
        continue

      try:
        # Extract and convert data from columns
        district = columns[1].strip()
        green_transport = float(columns[2].strip())
        public_transport = float(columns[3].strip())
        non_motorized = float(columns[4].strip())
        walking = float(columns[5].strip())
        bike = float(columns[6].strip())
        private_motorized = float(columns[7].strip())
        most_used_public_transport = float(columns[8].strip())

        # Create text description for embedding generation
        text = (f"{district}: "
                f"["
                f"綠運輸:{green_transport}%, 公共運具:{public_transport}%, 非機動運具:{non_motorized}%, "
                f"步行:{walking}%, 自行車(含公共):{bike}%, 私人機動運具:{private_motorized}%, "
                f"最常公共運具使用率:{most_used_public_transport}%"
                f"]")

        print(text)

        # Generate embedding vector for the text description
        embedding = generate_embedding(text)

        # Create TransportationData object and add to list
        data_rows.append(
            TransportationData(
                district=district,
                green_transport=green_transport,
                public_transport=public_transport,
                non_motorized=non_motorized,
                walking=walking,
                bike=bike,
                private_motorized=private_motorized,
                most_used_public_transport=most_used_public_transport,
                embedding=embedding,
            )
        )
      except ValueError as e:
        # Log error and skip invalid rows
        print(f"Error processing line: {line.strip()} - {e}")
        continue

    # If we have collected data, save to database
    if data_rows:
      # Clear existing records before bulk insert
      TransportationData.objects.all().delete()
      TransportationData.objects.bulk_create(data_rows)
