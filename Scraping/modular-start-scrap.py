import modular_scrap_course as scraper

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/apache-spark-mastery-data-engineering-pyspark",
    "Apache Spark Mastery",
    "Scraped_data/Modular_courses/Apache_Spark_Mastery.json"
)
print("Scraping completed for Apache Spark Mastery course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/aptitude-course-in-pune",
    "Aptitude Course",
    "Scraped_data/Modular_courses/Aptitude_Course_Details.json"
)

print("Scraping completed for Aptitude Course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/core-java-classes",
    "Core Java Classes",
    "Scraped_data/Modular_courses/Core_Java.json"
)
print("Scraping completed for Core Java Classes course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/aptitude-course-in-pune",
    "Aptitude",
    "Scraped_data/Modular_courses/Aptitude_Course_Details.json"
)
print("Scraping completed for Aptitude course.")

scraper.scrape_modular_courses("https://sunbeaminfo.in/modular-courses/data-structure-algorithms-using-java",
                               "Data Structures and Algorithms",
                                 "Scraped_data/Modular_courses/data_structures_algorithms_scrap.json"
                               )
print("Scraping completed for Data Structures and Algorithms course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/Devops-training-institute",
    "Dev Ops",
    "Scraped_data/Modular_courses/dev_ops_scrap.json"
)
print("Scraping completed for Dev Ops course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/dreamllm-training-institute-pune",
    "Dream LLM",
    "Scraped_data/Modular_courses/dream_llm_scrap.json"
)
print("Scraping completed for Dream LLM course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/machine-learning-classes",
    "Machine Learning",
    "Scraped_data/Modular_courses/machine_learning_scrap.json"
)
print("Scraping completed for Machine Learning course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mastering-generative-ai",
    "Mastering Generative AI",
    "Scraped_data/Modular_courses/mastering_gen_ai_scrap.json"
)
print("Scraping completed for Mastering Generative AI course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses.php?mdid=57",
    "Mastering MCQs",
    "Scraped_data/Modular_courses/mastering_mcqs_scrap.json"
)
print("Scraping completed for Mastering MCQs course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mern-full-stack-developer-course",
    "MERN (Full Stack) Development",
    "Scraped_data/Modular_courses/mern_full_stack_scrap.json"
)
print("Scraping completed for MERN Full Stack Development course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mlops-llmops-training-institute-pune",
    "MLOps & LLMOps",
    "Scraped_data/Modular_courses/mlops_llmops_scrap.json"
)
print("Scraping completed for MLOps & LLMOps course.")

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/python-classes-in-pune",
    "Python Development",
    "Scraped_data/Modular_courses/python_development_scrap.json"
)
print("Scraping completed for Python Development course.")