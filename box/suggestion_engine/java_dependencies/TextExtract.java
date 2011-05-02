import java.io.File;
import java.io.*;

import org.apache.poi.POITextExtractor;
import org.apache.poi.extractor.ExtractorFactory;
import org.apache.poi.openxml4j.exceptions.OpenXML4JException;
import org.apache.xmlbeans.XmlException;

public class TextExtract {
	public static void main(String[] args) {
		TextExtract te = new TextExtract();
		try {
			te.run(args[0]);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void run(String filename) throws XmlException, 
										OpenXML4JException, IOException {
		POITextExtractor textExtractor = 
			ExtractorFactory.createExtractor(new File("suggestion_engine/temp_files/" + filename));
			
		try {	
		    System.out.println(textExtractor.getText());
		} catch (Exception e) {
		    e.printStackTrace();
		}
	}
}