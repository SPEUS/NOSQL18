package de.haw;

import redis.clients.jedis.Jedis;
import java.io.*;

public class Main {

    public static void main(String[] args) {
        System.out.println("Lade plz.data ...");
        File plzFile = new File("plz.data");
        try (BufferedReader br = new BufferedReader(new FileReader(plzFile))){
            String dataSet = br.readLine();
            Jedis jedisClient = new Jedis();
            while(dataSet != null && !dataSet.trim().isEmpty()) {
                DataEntry parsedDataEntry = DataEntry.parseData(dataSet);
                jedisClient.hmset(parsedDataEntry.getId(), parsedDataEntry.getData());
                jedisClient.rpush(parsedDataEntry.getData().get("city"), parsedDataEntry.getId());
                dataSet = br.readLine();
            }
            jedisClient.close();
        } catch (FileNotFoundException e) {
            System.out.println("Datei plz.data nicht gefunden.");
        } catch (IOException e) {
            System.out.println("Fehler beim Einlesen der Datei.");
        }
        System.out.println("Alle Daten geladen!");
    }
}
