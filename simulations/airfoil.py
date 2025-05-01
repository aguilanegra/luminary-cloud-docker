import luminarycloud as lc
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Authenticate and set up the project
    project = lc.create_project("NACA 0012", "My first SDK project.")

    # Upload the mesh file
    mesh = project.upload_mesh("airfoil.lcmesh")
    mesh.wait()  # Wait for the mesh upload and processing to complete

    mesh_metadata = lc.get_mesh_metadata(mesh.id)

    # Create a simulation template from a JSON file
    sim_template = project.create_simulation_template("Airfoil Template", "simulation_template.json")

    # Create a simulation using the uploaded mesh and template
    simulation = project.create_simulation(mesh.id, "Airfoil Simulation", sim_template.id)

    # Wait for the simulation to complete and show that it's completed
    print("Simulation finished with status:", simulation.wait().name)

    with simulation.download_global_residuals() as stream:
        residuals_df = pd.read_csv(stream, index_col="Iteration index")
        # since this is a steady state simulation, we can drop these columns
        residuals_df = residuals_df.drop(["Time step", "Physical time"], axis=1)

    print(residuals_df)

    residuals_df.plot(logy=True, figsize=(12, 8)).get_figure().savefig("./residuals.png")

if __name__ == '__main__':
    main()
