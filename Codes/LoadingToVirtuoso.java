package Sweb;

import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStream;
import java.util.Properties;

import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.util.FileManager;

import virtuoso.jena.driver.VirtModel;
import virtuoso.jena.driver.VirtuosoQueryExecutionFactory;
import virtuoso.jena.driver.VirtuosoUpdateFactory;
import virtuoso.jena.driver.VirtuosoUpdateRequest;



public class LoadingToVirtuoso {
	public static void main(String[] args) {
		try {
			BufferedWriter writer = new BufferedWriter(
					new FileWriter("/User/Mittal/Desktop/OutputFile.txt"));
			Properties prop = new Properties();
			InputStream input = null;
			input = new FileInputStream("config.properties");
			prop.load(input);

			System.out.println(prop.getProperty("server"));
			Model model = VirtModel.openDatabaseModel("LoadingToVirtuoso", prop.getProperty("server"),
					prop.getProperty("database"), prop.getProperty("password"));

			String nfile = prop.getProperty("mittalLocation");
			InputStream in = FileManager.get().open(nfile);
			System.out.println("1");
			if (in == null) {
				throw new IllegalArgumentException("File: not found");
			}
			System.out.println("2");

			long startTime = System.currentTimeMillis();

			model.read(in, null, "TURTLE");

			System.out.println("\nexecute: CLEAR GRAPH <http://LoadingMittal>");
			String str1 = "CLEAR GRAPH <http://LoadingMittal>";
			VirtuosoUpdateRequest vur = VirtuosoUpdateFactory.create(str1, model);
			vur.exec();

			Query sparql2 = QueryFactory
					.create("SELECT (count(*) AS ?count) FROM <http://LoadingMittal> WHERE {?s ?p ?o}");
			QueryExecution vqe = VirtuosoQueryExecutionFactory.create(sparql2, model);
			ResultSet result = vqe.execSelect();
			while (result.hasNext()) {
				QuerySolution soln = result.nextSolution();
				int count = soln.getLiteral("count").getInt();
				System.out.println("Count = " + count);
				writer.write("Count: " + count);
				writer.write("\n");
			}
			long endTime = System.currentTimeMillis();
			long totalTimeTaken = (endTime - startTime);
			writer.write("Total time for loading in milliseconds: " + totalTimeTaken);
			System.out.println(totalTimeTaken);
			writer.close();

		} catch (Exception e) {
			System.out.println("Ex=" + e);
		}

	}

}