File: simple-slf4j-conflict/README.md

Simple SLF4J Version Conflict

Scenario

ch.qos.logback:logback-classic:1.2.3 brings in slf4j-api:1.7.25

org.slf4j:slf4j-simple:1.7.30 brings in slf4j-api:1.7.30
Maven’s “nearest wins” strategy will choose one version and omit the other.

POM changes required to simulate the issue

Open pom.xml and add a direct dependency on slf4j-simple version 1.7.30:
<dependency>
<groupId>org.slf4j</groupId>
<artifactId>slf4j-simple</artifactId>
<version>1.7.30</version>
</dependency>

Ensure you still have the Logback dependency:
<dependency>
<groupId>ch.qos.logback</groupId>
<artifactId>logback-classic</artifactId>
<version>1.2.3</version>
</dependency>

After these edits, your dependencies are:

ch.qos.logback:logback-classic:1.2.3 (→ slf4j-api:1.7.25)

org.slf4j:slf4j-simple:1.7.30 (→ slf4j-api:1.7.30)

Code changes required in App.java

Import SLF4J:
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

Declare and use the SLF4J logger:
public class App {
private static final Logger LOG = LoggerFactory.getLogger(App.class);
public static void main(String[] args) {
LOG.info("Hello from SLF4J conflict demo!");
}
}

Steps

Simulate the conflict
Run:
mvn dependency:tree -Dverbose -Dincludes=org.slf4j:slf4j-api
You should see output similar to:
+- ch.qos.logback:logback-classic:1.2.3
| - org.slf4j:slf4j-api:1.7.25
- org.slf4j:slf4j-simple:1.7.30
- org.slf4j:slf4j-api:1.7.30 (omitted for conflict with 1.7.25)

Explain what happened
Maven saw two different slf4j-api versions. Because of “nearest wins,” it chose 1.7.25 (from Logback) and omitted 1.7.30.

Apply the fix

Option A – force the desired version via dependencyManagement

Add this block under the project element (before <dependencies>):
<dependencyManagement>
<dependencies>
<dependency>
<groupId>org.slf4j</groupId>
<artifactId>slf4j-api</artifactId>
<version>1.7.30</version>
</dependency>
</dependencies>
</dependencyManagement>

Option B – exclude the older API from the Logback dependency

Change the logback-classic entry in your dependencies section to:
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

Leave slf4j-simple:1.7.30 unchanged.

Verify the fix
Re-run:
mvn dependency:tree -Dverbose -Dincludes=org.slf4j:slf4j-api
You should now see only:
- org.slf4j:slf4j-simple:1.7.30
- org.slf4j:slf4j-api:1.7.30

Optional – run the demo code
mvn clean compile exec:java -Dexec.mainClass=com.example.App
Expected output:
[main] INFO com.example.App - Hello from SLF4J conflict demo!
