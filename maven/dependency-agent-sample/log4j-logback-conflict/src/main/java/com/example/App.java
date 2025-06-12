package com.example;

// old SLF4J imports commented out
// import org.slf4j.Logger;
// import org.slf4j.LoggerFactory;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class App {
    // replace SLF4J Logger with Commons-Logging Log
    private static final Log LOG = LogFactory.getLog(App.class);

    public static void main(String[] args) {
        LOG.info("Hello from conflict demo!");
    }
}
