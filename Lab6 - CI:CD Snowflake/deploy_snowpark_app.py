#!/usr/bin/env python
import sys
import os
import yaml
import subprocess
import argparse

def deploy_snowpark_app(directory_path, env):
    """Deploy a Snowpark application to Snowflake"""
    print(f"Deploying Snowpark app in {directory_path} to {env} environment")
    
    # Read the project configuration
    with open(f"{directory_path}/snowflake.yml", "r") as file:
        config = yaml.safe_load(file)
    
    # Read environment-specific settings
    env_config_path = f"{os.path.dirname(os.path.dirname(directory_path))}/config/{env}.yml"
    with open(env_config_path, "r") as file:
        env_config = yaml.safe_load(file)
    
    # Create a modified config with environment values
    modified_config = config.copy()
    # Replace placeholders with environment values
    for function in modified_config.get('snowpark', {}).get('functions', []):
        function['database'] = env_config['database_name']
    
    # Write the modified config back to a temporary file
    temp_config_path = f"{directory_path}/snowflake_temp.yml"
    with open(temp_config_path, "w") as file:
        yaml.dump(modified_config, file)
    
    # Build and deploy using Snow CLI
    os.chdir(directory_path)
    
    # Set environment variables for snow CLI
    os.environ["SNOWFLAKE_WAREHOUSE"] = env_config["warehouse_name"]
    
    # Build the Snowpark app
    print("Building Snowpark application...")
    build_result = subprocess.run(["snow", "snowpark", "build"], capture_output=True, text=True)
    print(build_result.stdout)
    if build_result.returncode != 0:
        print(f"Error during build: {build_result.stderr}")
        return False
    
    # Deploy the Snowpark app
    print("Deploying Snowpark application...")
    deploy_result = subprocess.run(["snow", "snowpark", "deploy", "--replace"], 
                                  capture_output=True, text=True)
    print(deploy_result.stdout)
    if deploy_result.returncode != 0:
        print(f"Error during deployment: {deploy_result.stderr}")
        return False
    
    # Clean up
    os.remove(temp_config_path)
    print(f"Successfully deployed to {env} environment")
    return True

def main():
    parser = argparse.ArgumentParser(description='Deploy Snowpark application to Snowflake')
    parser.add_argument('--env', choices=['dev', 'prod'], default='dev',
                        help='Environment to deploy to (dev or prod)')
    args = parser.parse_args()
    
    # Get the path to the data_masker app
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Deploy the data masker app
    success = deploy_snowpark_app(f"{root_dir}/src/data_masker", args.env)
    if success:
        print("Deployment completed successfully")
    else:
        print("Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
