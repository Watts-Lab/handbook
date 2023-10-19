
[Scaling and Partitioning Data](https://aws.amazon.com/blogs/big-data/best-practices-to-scale-apache-spark-jobs-and-partition-data-with-aws-glue/)
- AWS Glue provides a serverless environment to prepare (extract and transform) and load large amounts of datasets from a variety of sources for analytics and data processing with Apache Spark ETL jobs
- Two scaling methods:
    - The first allows you to horizontally scale out Apache Spark applications for large splittable datasets. 
    - The second allows you to vertically scale up memory-intensive Apache Spark applications with the help of new AWS Glue worker types
- Understanding AWS Glue worker types
    - Standard, G.1X, and G.2X
    - AWS Glue jobs that need high memory or ample disk space to store intermediate shuffle output can benefit from vertical scaling (more G1.X or G2.x workers)
- Horizontal scaling for splittable datasets
    - A file split is a portion of a file that a Spark task can read and process independently on an AWS Glue worker


[Glue Bookmarks and Glue Optimized Parquet Writer](https://aws.amazon.com/blogs/big-data/load-data-incrementally-and-optimized-parquet-writer-with-aws-glue/)
- Glue Optimized Apache Parquet writer
    - Unlike the default Apache Spark Parquet writer, it does not require a pre-computed schema or schema that is inferred by performing an extra scan of the input dataset. --> `glueparquet`
    - The AWS Glue Parquet writer also enables schema evolution by supporting the deletion and addition of new columns


[Glue automatic code generation and Workflows](https://aws.amazon.com/blogs/big-data/simplify-data-pipelines-with-aws-glue-automatic-code-generation-and-workflows/)
- ...

[Optimize Memory Management](https://aws.amazon.com/blogs/big-data/optimize-memory-management-in-aws-glue/)
- ...

[Developing Glue ETL jobs locally using a Docker container](https://aws.amazon.com/blogs/big-data/developing-aws-glue-etl-jobs-locally-using-a-container/)
- AWS Glue is built on top of Apache Spark and therefore uses all the strengths of open-source technologies. 
- AWS Glue comes with many improvements on top of Apache Spark and has its own ETL libraries that can fast-track the development process and reduce boilerplate code.

```
// docker image pull
docker pull amazon/aws-glue-libs:glue_libs_3.0.0_image_01

// run docker image (REPL)
docker run -it -v ~/.aws:/home/glue_user/.aws -e AWS_ACCESS_KEY_ID=... -e AWS_SECRET_ACCESS_KEY=... -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 --name glue_pyspark amazon/aws-glue-libs:glue_libs_3.0.0_image_01 pyspark


// check for interactive dev endpoints 
aws glue list-dev-endpoints
```

