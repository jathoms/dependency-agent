# OVERVIEW
This sample shows how Commons-Logging picks whichever backend it finds first (Log4j or Logback) and how excluding Log4j forces Commons-Logging to bind to Logback.

## COMMON CODE (src/main/java/com/example/App.java)
```java
// SLF4J imports commented out
// import org.slf4j.Logger;
// import org.slf4j.LoggerFactory;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class App {
    private static final Log LOG = LogFactory.getLog(App.class);

    public static void main(String[] args) {
        LOG.info("Hello from conflict demo!");
    }
}
```

---

## BROKEN SCENARIO
**Scenario:**
- `commons-logging:1.0.4` provides the API
- direct dependency on `log4j:1.2.17`
- `logback-classic:1.2.11` (with `slf4j-api:1.7.x`) also on classpath

At runtime, Commons-Logging binds to Log4j (no `log4j.properties` present) and you see WARNs but no log output.

### POM (`log4j-logback-conflict-broken/pom.xml`)
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>log4j-logback-conflict-broken</artifactId>
  <version>1.0.0-SNAPSHOT</version>

  <dependencies>
    <dependency>
      <groupId>log4j</groupId>
      <artifactId>log4j</artifactId>
      <version>1.2.17</version>
    </dependency>

    <dependency>
      <groupId>commons-logging</groupId>
      <artifactId>commons-logging</artifactId>
      <version>1.0.4</version>
    </dependency>

    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.2.11</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
      </plugin>
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>3.1.0</version>
        <configuration>
          <mainClass>com.example.App</mainClass>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

### Steps to reproduce
```bash
mvn -f pom-broken.xml clean compile
```

### Expected output
```
log4j:WARN No appenders could be found for logger (com.example.App).
log4j:WARN Please initialize the log4j system properly.
log4j:WARN See http://logging.apache.org/log4j/1.2/faq.html#noconfig for more info.
```

### Optional
```bash
mvn dependency:tree
# → shows log4j:1.2.17 present
```

---

## FIXED SCENARIO
**Scenario:**
- `commons-logging:1.0.4` (excluding Log4j) provides the API
- `logback-classic:1.2.11` (via SLF4J) is the backend

By removing the direct Log4j dependency and excluding it from Commons-Logging, Commons-Logging binds to Logback and emits logs correctly.

### POM (`log4j-logback-conflict-fixed/pom.xml`)
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>log4j-logback-conflict-fixed</artifactId>
  <version>1.0.0-SNAPSHOT</version>

  <dependencies>
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
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
      </plugin>
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>3.1.0</version>
        <configuration>
          <mainClass>com.example.App</mainClass>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

### Steps to verify
```bash
mvn clean compile exec:java
```

### Expected output
```
[main] INFO com.example.App - Hello from conflict demo!
```

### Optional
```bash
mvn dependency:tree
# → log4j:1.2.17 is no longer listed
```<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>log4j-logback-conflict-broken</artifactId>
    <version>1.0.0-SNAPSHOT</version>

    <properties>
        <!-- Encoding and version properties -->
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.release>21</maven.compiler.release>
        <maven.compiler.pluginVersion>3.10.1</maven.compiler.pluginVersion>
        <exec.pluginVersion>3.1.0</exec.pluginVersion>
        <enforcer.pluginVersion>3.3.0</enforcer.pluginVersion>
    </properties>

    <dependencies>
        <!-- Direct Log4j 1.x dependency causes Commons-Logging to bind to Log4j -->
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.17</version>
        </dependency>

        <!-- Commons-Logging brings in log4j via transitive -->
        <dependency>
            <groupId>commons-logging</groupId>
            <artifactId>commons-logging</artifactId>
            <version>1.0.4</version>
        </dependency>

        <!-- Logback is also on the classpath, but loses the “race” -->
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.11</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Enforce Maven version 3.8.4+ -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-enforcer-plugin</artifactId>
                <version>${enforcer.pluginVersion}</version>
                <executions>
                    <execution>
                        <id>enforce-maven</id>
                        <goals>
                            <goal>enforce</goal>
                        </goals>
                        <configuration>
                            <rules>
                                <requireMavenVersion>
                                    <version>[3.8.4,)</version>
                                    <message>Requires Maven 3.8.4 or later.</message>
                                </requireMavenVersion>
                            </rules>
                        </configuration>
                    </execution>
                </executions>
            </plugin>

            <!-- Compile with Java 21 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${maven.compiler.pluginVersion}</version>
                <configuration>
                    <release>${maven.compiler.release}</release>
                </configuration>
            </plugin>

            <!-- Execute main class -->
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>${exec.pluginVersion}</version>
                <configuration>
                    <mainClass>com.example.App</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
