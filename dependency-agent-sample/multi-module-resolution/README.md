File: multi-module-resolution/README.md

Multi-Module Version Management

This sample shows how a parent POM can enforce a newer Jackson version across child modules, overriding a transitive older version.

Project structure
multi-module-resolution/
├── pom.xml ← parent POM with dependencyManagement for Jackson 2.14.0
├── core/ ← core module uses Jackson
└── web/ ← web module pulls in Spring Boot (defaults to Jackson 2.9.8)

Steps

Simulate the “broken” state
• Open multi-module-resolution/pom.xml and comment out the entire <dependencyManagement> block that pins Jackson to 2.14.0.
• Save the file.
• In a terminal run:
cd multi-module-resolution/web
mvn dependency:tree | grep jackson-databind
You should see:
com.fasterxml.jackson.core:jackson-databind:jar:2.9.8:compile

Inspect the effective POM in the broken state
In the same directory run:
mvn help:effective-pom | grep "<jackson-databind>" -A1
You will see <version>2.9.8</version> for jackson-databind.

Apply/confirm the fix
• Re-open multi-module-resolution/pom.xml and uncomment the <dependencyManagement> block (restore Jackson 2.14.0 override).
• From the multi-module root run:
cd .. (to multi-module-resolution)
mvn clean install
• Go back into web and re-run:
cd web
mvn dependency:tree | grep jackson-databind
Now you should see:
com.fasterxml.jackson.core:jackson-databind:jar:2.14.0:compile

Inspect the effective POM in the fixed state
Still in web run:
mvn help:effective-pom | grep "<jackson-databind>" -A1
You will see <version>2.14.0</version>, proving the parent override is honored.

Tip
Always run mvn help:effective-pom when you add or change a parent POM or <dependencyManagement> section, to confirm Maven is applying your version overrides.
