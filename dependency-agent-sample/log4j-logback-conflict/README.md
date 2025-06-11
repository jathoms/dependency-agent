File: log4j-logback-conflict/README.md

Log4j 1.x vs. Logback Conflict

Scenario

commons-logging 1.0.4 provides the logging API

You have a direct dependency on log4j:1.2.17

logback-classic 1.2.11 brings in SLF4J + slf4j-api:1.7.x
At runtime Commons-Logging will bind to whichever backend it finds on the classpath. With Log4j present and no log4j.properties, you get WARNs and no actual log output.

Code changes required to simulate the issue

In src/main/java/com/example/App.java, replace the SLF4J logger with Commons-Logging:
• Comment out or remove these lines:
// import org.slf4j.Logger;
// import org.slf4j.LoggerFactory;
// private static final Logger LOG = LoggerFactory.getLogger(App.class);
• Add these lines at the top of the file:
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
• Replace the logger declaration with:
private static final Log LOG = LogFactory.getLog(App.class);
• Keep the main method as:
public static void main(String[] args) {
LOG.info("Hello from conflict demo!");
}

Steps

Simulate the broken state
Run:
mvn clean compile exec:java -Dexec.mainClass=com.example.App
Expected output:
log4j:WARN No appenders could be found for logger (com.example.App).
log4j:WARN Please initialize the log4j system properly.
log4j:WARN See http://logging.apache.org/log4j/1.2/faq.html#noconfig for more info.

Apply the fix (remove the direct Log4j dependency)
In pom.xml, delete or comment out the entire Log4j dependency block:
<dependency>
<groupId>log4j</groupId>
<artifactId>log4j</artifactId>
<version>1.2.17</version>
</dependency>
Ensure you still have:
<dependency>
<groupId>commons-logging</groupId>
<artifactId>commons-logging</artifactId>
<version>1.0.4</version>
<exclusions>
<exclusion>
<groupId>log4j</groupId>
<artifactId>log4j</artifactId>
</exclusion>
</exclusions>
</dependency>
<dependency>
<groupId>ch.qos.logback</groupId>
<artifactId>logback-classic</artifactId>
<version>1.2.11</version>
</dependency>

Verify the fix
Run:
mvn clean compile exec:java -Dexec.mainClass=com.example.App
Expected output:
[main] INFO com.example.App - Hello from conflict demo!

Optional: confirm classpath changes

Before fix you saw log4j:log4j:1.2.17 in mvn dependency:tree

After fix it is gone, leaving only commons-logging and logback-classic
