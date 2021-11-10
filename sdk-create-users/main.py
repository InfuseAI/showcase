import argparse
from src.batch_create_users import BatchCreateUsers

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--primehub_config",
        help="Recreate PrimeHub config file.",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-u", "--cluster_url",
        help="PrimeHub cluster URL.", type=str, required=True
    )
    parser.add_argument(
        "-f",
        "--file_path",
        help="PrimeHub account csv file.",
        type=str,
        default="./data/user_list.csv",
    )
    args = parser.parse_args()
    batch_create_users = BatchCreateUsers(
                            args.cluster_url,
                            args.primehub_config
                        )
    batch_create_users.batch_create_users(args.file_path)
