import modular_scrap_course as scraper

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/apache-spark-mastery-data-engineering-pyspark",
    "Apache Spark Mastery",
    "apache_spark_mastery_scrap.json"
)
print("Scraping completed for Apache Spark Mastery course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/core-java-classes",
    "Core Java Classes",
    "core_java_classes_scrap.json"
)
print("Scraping completed for Core Java Classes course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/aptitude-course-in-pune",
    "Aptitude",
    "Aptitude_Course_Details.json"
)
print("Scraping completed for Aptitude course.")



scraper.scrape_modular_courses("https://sunbeaminfo.in/modular-courses/data-structure-algorithms-using-java",
                               "Data Structures and Algorithms",
                                 "data_structures_algorithms_scrap.json"
                               )
print("Scraping completed for Data Structures and Algorithms course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/Devops-training-institute",
    "Dev Ops",
    "dev_ops_scrap.json"
)
print("Scraping completed for Dev Ops course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/dreamllm-training-institute-pune",
    "Dream LLM",
    "dream_llm_scrap.json"
)
print("Scraping completed for Dream LLM course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/machine-learning-classes",
    "Machine Learning",
    "machine_learning_scrap.json"
)
print("Scraping completed for Machine Learning course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mastering-generative-ai",
    "Mastering Generative AI",
    "mastering_gen_ai_scrap.json"
)
print("Scraping completed for Mastering Generative AI course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses.php?mdid=57",
    "Mastering MCQs",
    "mastering_mcqs_scrap.json"
)
print("Scraping completed for Mastering MCQs course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mern-full-stack-developer-course",
    "MERN (Full Stack) Development",
    "mern_full_stack_scrap.json"
)
print("Scraping completed for MERN Full Stack Development course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mlops-llmops-training-institute-pune",
    "MLOps & LLMOps",
    "mlops_llmops_scrap.json"
)
print("Scraping completed for MLOps & LLMOps course.")


scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/python-classes-in-pune",
    "Python Development",
    "python_development_scrap.json"
)
print("Scraping completed for Python Development course.")
