# OVERVIEW

This sample demonstrates a version conflict between two SLF4J implementations on the classpath: Logback Classic (bringing `slf4j-api:1.7.25`) and SLF4J Simple (bringing `slf4j-api:1.7.30`). Maven’s “nearest wins” strategy will choose one API version and omit the other. Below you’ll find two scenarios: **Broken** (conflict reproduces) and **Fixed** (conflict resolved).

## COMMON CODE (src/main/java/com/example/App.java)

```java
package com.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class App {
    private static final Logger LOG = LoggerFactory.getLogger(App.class);

    public static void main(String[] args) {
        LOG.info("Hello from SLF4J conflict demo!");
    }
}
```

---

## BROKEN SCENARIO

**Scenario:**

* `logback-classic:1.2.3` → brings `slf4j-api:1.7.25`
* `slf4j-simple:1.7.30` → brings `slf4j-api:1.7.30`

Maven picks `slf4j-api:1.7.25` (from Logback) and omits `1.7.30`, leading to unexpected behavior or mismatch.

### POM (`simple-slf4j-conflict-broken/pom.xml`)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example.dependencyagent</groupId>
  <artifactId>simple-slf4j-conflict-broken</artifactId>
  <version>1.0.0-SNAPSHOT</version>

  <dependencies>
    <!-- A: Logback Classic brings slf4j-api:1.7.25 -->
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.2.3</version>
    </dependency>

    <!-- B: SLF4J Simple brings slf4j-api:1.7.30 -->
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-simple</artifactId>
      <version>1.7.30</version>
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
mvn dependency:tree -Dverbose -Dincludes=org.slf4j:slf4j-api
```

### Expected dependency-tree excerpt

```text
[INFO] +- ch.qos.logback:logback-classic:1.2.3
[INFO] |  \- org.slf4j:slf4j-api:1.7.25
[INFO] \- org.slf4j:slf4j-simple:1.7.30
[INFO]    \- org.slf4j:slf4j-api:1.7.30 (omitted for conflict with 1.7.25)
```

**Explanation:** Maven saw two versions of `slf4j-api`; “nearest wins” chose `1.7.25` and omitted `1.7.30`.

---

## FIXED SCENARIO

**Goal:** Ensure `slf4j-api:1.7.30` is the only API version on the classpath.

### Option A – Force version via `dependencyManagement` (`simple-slf4j-conflict-fixed/pom.xml`)

```xml
<dependencyManagement>
  <dependencies>
    <!-- Force slf4j-api to 1.7.30 -->
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>1.7.30</version>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.3</version>
  </dependency>
  <dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-simple</artifactId>
    <version>1.7.30</version>
  </dependency>
</dependencies>
```

### Option B – Exclude older API from Logback

```xml
<dependencies>
  <dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.3</version>
    <exclusions>
      <exclusion>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
      </exclusion>
    </exclusions>
  </dependency>
  <dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-simple</artifactId>
    <version>1.7.30</version>
  </dependency>
</dependencies>
```

### Verify the fix

1. Dependency tree:

   ```bash
   mvn dependency:tree -Dverbose -Dincludes=org.slf4j:slf4j-api
   ```

   **Expect to see only:**

   ```text
   org.slf4j:slf4j-simple:1.7.30
   org.slf4j:slf4j-api:1.7.30
   ```

2. Run the app:

   ```bash
   mvn clean compile exec:java -Dexec.mainClass=com.example.App
   ```

   **Expected output:**

   ```text
   [main] INFO com.example.App - Hello from SLF4J conflict demo!
   ```
