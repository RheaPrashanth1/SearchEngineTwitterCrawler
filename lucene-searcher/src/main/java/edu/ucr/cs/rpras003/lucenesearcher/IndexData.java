package edu.ucr.cs.rpras003.lucenesearcher;

import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;
import java.io.*;
import java.util.StringTokenizer;
import java.util.Scanner;

import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TopDocs;
import com.google.gson.Gson;
import org.apache.lucene.queryparser.classic.QueryParser;


import java.nio.file.Path;
import java.nio.file.Paths;



//import org.apache.lucene.queryparser.QueryParser;



@RestController
@RequestMapping("/api")
@CrossOrigin("*")
public class IndexData {

        

  @GetMapping("/articles")
    public final static String[] searchTheIndex( @RequestParam(required=false, defaultValue="")String query)  throws Exception, IOException{
     String[] emptyStr = new String[10];
      if (query.isEmpty()) {
        
        return emptyStr;
     }
    
      Analyzer a = new StandardAnalyzer();
        Path pg = Paths.get("/Users/rheaprashanth/Documents/VScode/SearchEngineTwitter/PythonRandomShit/Index");
        DirectoryReader ireader = DirectoryReader.open(FSDirectory.open(pg));
        IndexSearcher searcher = new IndexSearcher(ireader); //creates searcher 
       
   
        try{ 
    

        QueryParser qp = new QueryParser("text",a);
        Query q = qp.parse(query);
        TopDocs docs = searcher.search(q, 10);
        ScoreDoc[] results = docs.scoreDocs; //returns array of doc # and doc score
        String[] Tweets = new String[results.length];
        System.out.println("Results length is:" );
      
        System.out.println(results.length);
        for(int i =0; i < results.length ; ++i) {
           // System.out.println("in for loop");
            Document hitDoc = searcher.doc(results[i].doc);
            String retString = ("Tweet result number " + (i + 1)  + ": @:" + hitDoc.get("screenName") + " said: "  + hitDoc.get("text")  + " - Tweeted on: " + hitDoc.get("date")  + ". Tweet score is: " + results[i].score + ".\n").replace("\n", "") + "\n"  ;
           // Gson gson = new Gson();
         //   json = gson.toJson(obj); 
      
            // String retString =  hitDoc.get("text");
           Tweets[i] = retString;
          
            
           
          }
          

          return Tweets;
        }
        catch (Exception e) {
			e.printStackTrace();
        }   
        finally {
		ireader.close();
		}
		return null;
    
  }

}


