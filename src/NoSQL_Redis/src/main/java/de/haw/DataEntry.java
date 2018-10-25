package de.haw;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DataEntry {
    private static Pattern idRegex;
    private static Pattern cityRegex;
    private static Pattern locRegex;
    private static Pattern popRegex;
    private static Pattern stateRegex;
    private static List<Pattern> valuePatterns;

    private String id;
    private Map<String, String> data;

    static {
        idRegex = Pattern.compile("\"_id\":\"(.*?)\"");
        cityRegex = Pattern.compile("\"(city)\":\"(.*?)\"");
        locRegex = Pattern.compile("\"(loc)\":\\[(.*?)\\]");
        popRegex = Pattern.compile("\"(pop)\":(.*?),");
        stateRegex = Pattern.compile("\"(state)\":\"(.*?)\"");

        valuePatterns = new ArrayList<>();
        valuePatterns.add(cityRegex);
        valuePatterns.add(locRegex);
        valuePatterns.add(popRegex);
        valuePatterns.add(stateRegex);
    }

    public static DataEntry parseData(String rawData) {
        //Entfernt geschweifte Klammern und Leerzeichen
        String cleanedRawData = rawData.substring(1,rawData.length()-1).replaceAll("\\s", "");
        String id = null;
        Map<String, String> values = new HashMap<>();
        //Liest _id aus
        Matcher m = idRegex.matcher(cleanedRawData);
        m.find();
        id = m.group(1);
        //Liest restliche Werte
        for(Pattern valuePattern : valuePatterns) {
            m = valuePattern.matcher(cleanedRawData);
            m.find();
            values.put(m.group(1), m.group(2));
        }
        return new DataEntry(id, values);
    }

    private DataEntry() {

    }

    private DataEntry(String id, Map<String, String> data) {
        this.id = id;
        this.data = data;
    }

    public String getId() {
        return id;
    }

    public Map<String, String> getData() {
        return data;
    }
}
