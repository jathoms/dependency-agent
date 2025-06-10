package com.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.slf4j.spi.LoggingEventBuilder;

public class App {
    public static void main(String[] args) {
        System.out.println("Hello World!");

        Logger logger = LoggerFactory.getLogger(App.class);

        // LoggingEventBuilder is as of slf4j 2.0.0
        LoggingEventBuilder builder = logger.atInfo()
                .addKeyValue("user", "alice");
        builder.log("User {} performed an action", "alice");
    }
}
