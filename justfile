go:
	uv build && uv run depguy

mvn1:
	cd maven/demo-app && mvn clean install

mvnbroken1:
	cd maven/demo-app && mvn -f pom_that_do_not_work.xml clean install