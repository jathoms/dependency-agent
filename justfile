# Justfile for Dependency Agent Samples

# UV application commands
go:
    uv build && uv run depguy

# Demo app Maven commands
mvn1:
    cd maven/demo-app && mvn clean install

mvnbroken1:
	cd maven/demo-app && mvn -f pom_that_do_not_work.xml clean install

# Log4j vs Logback conflict sample

log4j_broken_build:
	cd maven/dependency-agent-sample/log4j-logback-conflict && mvn -f pom-broken.xml clean compile

log4j_broken_run:
	cd maven/dependency-agent-sample/log4j-logback-conflict && mvn -f pom-broken.xml clean compile exec:java -Dexec.mainClass=com.example.App

log4j_fixed_build:
	cd maven/dependency-agent-sample/log4j-logback-conflict && mvn clean compile

log4j_fixed_run:
	cd maven/dependency-agent-sample/log4j-logback-conflict && mvn clean compile exec:java -Dexec.mainClass=com.example.App

# Multi-module Jackson override sample

mmr_broken_build:
	cd maven/dependency-agent-sample/multi-module-resolution && mvn -f pom-broken.xml clean install

mmr_fixed_build:
	cd maven/dependency-agent-sample/multi-module-resolution && mvn clean install

mmr_broken_compile_web:
	cd maven/dependency-agent-sample/multi-module-resolution/web && mvn -f ../pom-broken.xml clean compile

mmr_fixed_compile_web:
	cd maven/dependency-agent-sample/multi-module-resolution/web && mvn clean compile
	
# Simple SLF4J conflict sample

slf4j_broken_build:
	cd maven/dependency-agent-sample/simple-slf4j-conflict && mvn -f pom-broken.xml clean compile

slf4j_broken_run:
	cd maven/dependency-agent-sample/simple-slf4j-conflict && mvn -f pom-broken.xml clean compile exec:java -Dexec.mainClass=com.example.App

slf4j_fixed_build:
	cd maven/dependency-agent-sample/simple-slf4j-conflict && mvn clean compile

slf4j_fixed_run:
	cd maven/dependency-agent-sample/simple-slf4j-conflict && mvn clean compile exec:java -Dexec.mainClass=com.example.App
