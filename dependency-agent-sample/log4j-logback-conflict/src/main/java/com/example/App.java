package com.example;

//import org.slf4j.Logger;
//import org.slf4j.LoggerFactory;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class App {
//    private static final Logger LOG = LoggerFactory.getLogger(App.class);
    private static final Log LOG = LogFactory.getLog(App.class);
    public static void main(String[] args) {
        LOG.info("Hello from conflict demo!");
    }
}
