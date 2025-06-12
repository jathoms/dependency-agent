# Multi-Module Version Management

This sample demonstrates how a parent POM can enforce a newer Jackson version across child modules, overriding a transitive older version provided by individual modules.

## Project structure

```
multi-module-resolution/
├── pom-broken.xml      ← parent POM **without** Jackson override (broken)
├── pom.xml             ← parent POM **with** Jackson 2.14.0 override (fixed)
├── core/
│   ├── pom-broken.xml  ← core module inheriting broken parent
│   └── pom.xml         ← core module inheriting fixed parent
└── web/
    ├── pom-broken.xml  ← web module inheriting broken parent
    └── pom.xml         ← web module inheriting fixed parent
```

---

## Parent POMs

### Broken Parent (`pom-broken.xml`)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.example.dependencyagent</groupId>
    <artifactId>dependency-agent-samples</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <relativePath>../pom.xml</relativePath>
  </parent>

  <groupId>com.example.multi</groupId>
  <artifactId>multi-module-resolution</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>

  <modules>
    <module>core</module>
    <module>web</module>
  </modules>

  <!-- BROKEN: no dependencyManagement override → default Jackson versions used -->
</project>
```

### Fixed Parent (`pom.xml`)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.example.dependencyagent</groupId>
    <artifactId>dependency-agent-samples</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <relativePath>../pom.xml</relativePath>
  </parent>

  <groupId>com.example.multi</groupId>
  <artifactId>multi-module-resolution</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>

  <modules>
    <module>core</module>
    <module>web</module>
  </modules>

  <!-- FIXED: enforce Jackson 2.14.0 across all modules -->
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.14.0</version>
      </dependency>
      <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-core</artifactId>
        <version>2.14.0</version>
      </dependency>
      <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-annotations</artifactId>
        <version>2.14.0</version>
      </dependency>
    </dependencies>
  </dependencyManagement>
</project>
```

---

## Module POMs

Both `core` and `web` modules have parallel POMs inheriting either `pom-broken.xml` or `pom.xml`.

### Core Module

#### Broken (`core/pom-broken.xml`)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.example.multi</groupId>
    <artifactId>multi-module-resolution</artifactId>
    <version>1.0.0</version>
    <relativePath>../pom-broken.xml</relativePath>
  </parent>

  <artifactId>core</artifactId>

  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.9.8</version>
    </dependency>
  </dependencies>
</project>
```

#### Fixed (`core/pom.xml`)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.example.multi</groupId>
    <artifactId>multi-module-resolution</artifactId>
    <version>1.0.0</version>
    <relativePath>../pom.xml</relativePath>
  </parent>

  <artifactId>core</artifactId>

  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
    </dependency>
  </dependencies>
</project>
```

### Web Module

#### Broken (`web/pom-broken.xml`)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.example.multi</groupId>
    <artifactId>multi-module-resolution</artifactId>
    <version>1.0.0</version>
    <relativePath>../pom-broken.xml</relativePath>
  </parent>

  <artifactId>web</artifactId>

  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.9.8</version>
    </dependency>
  </dependencies>
</project>
```

#### Fixed (`web/pom.xml`)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.example.multi</groupId>
    <artifactId>multi-module-resolution</artifactId>
    <version>1.0.0</version>
    <relativePath>../pom.xml</relativePath>
  </parent>

  <artifactId>web</artifactId>

  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
    </dependency>
  </dependencies>
</project>
```

---

## How to run

### Broken scenario

```powershell
cd multi-module-resolution
mvn -f pom-broken.xml clean install
mvn -f pom-broken.xml -pl web dependency:tree | findstr "jackson-databind"
mvn -f pom-broken.xml -pl web help:effective-pom
```

### Fixed scenario

```powershell
cd multi-module-resolution
mvn -f pom.xml clean install
mvn -f pom.xml -pl web dependency:tree | findstr "jackson-databind"
mvn -f pom.xml -pl web help:effective-pom
```

---

**Tip:** Use `findstr` on Windows to filter Maven output:

```powershell
mvn <goals> | findstr "jackson-databind"
```
