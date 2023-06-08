# Simple Clustered Web Service CloudFormation Template

This README provides an overview of the CloudFormation template code and its resources. The stack includes various AWS resources, and sets up a basic infrastructure with a VPC, subnets, load balancer, auto scaling group, and a Dockerized Flask application running on EC2 instances.

## Parameters <a name="parameters"></a>

The CloudFormation template includes the following parameters:

- `InstanceType`: The EC2 instance type for the launch template.
- `OperatingSystem`: Selects the operating system for the EC2 instance.
- `TemplateBucketName`: The S3 bucket name where the CloudFormation template and app files are stored (_only the name not the full URL_).
- `EmailAddress`: The email address to subscribe to the SNS topic.

## Mappings

The template includes mappings for region AMIs and availability zones. These mappings provide AMI IDs and availability zone names based on the selected AWS region and operating system. (Feel free to add more if you want to use the stack in different regions.)

## Resources

The template creates the following resources:

### VPC and Subnets

- `VPC`: Creates a VPC resource with the specified CIDR block and tags.
- `Subnet1` and `Subnet2`: Create two public subnets within the VPC with specified CIDR blocks, availability zones, and tags.

### Internet Gateway and Route Table

- `InternetGateway`: Creates an internet gateway resource with tags.
- `VPCGatewayAttachment`: Attaches the internet gateway to the VPC.
- `RouteTable`: Creates a route table resource associated with the VPC.
- `InternetRoute`: Creates a route in the route table for internet access.
- `Subnet1RouteTableAssociation` and `Subnet2RouteTableAssociation`: Associates the subnets with the route table.

### Security Groups

- `SecurityGroup`: Creates a security group for EC2 instances with inbound rules for HTTP and SSH access.
- `LoadBalancerSecurityGroup`: Creates a security group for the load balancer with inbound rules for HTTP access from the security group of EC2 instances.

### Load Balancer

- `LoadBalancer`: Creates an application load balancer with the specified subnets, security groups, and tags.
- `TargetGroup`: Creates a target group for the load balancer with health check settings.
- `Listener`: Creates a listener for the load balancer with default actions forwarding to the target group.

### EC2 Instance

- `NetworkInterface`: Creates a network interface attached to Subnet1 with specified security group and tags.
- `EC2Role` and `EC2RolePolicy`: Create an IAM role and policy for EC2 instances to access S3.
- `InstanceProfile`: Creates an instance profile for the launch template with the specified role.
- `LaunchTemplate`: Creates a launch template with the specified image, instance type, network interface, IAM instance profile, and user data. The user data script installs Docker, creates a Flask application file, a requirements.txt file, and a Dockerfile, builds a Docker image, and runs a Docker container with the Flask application.

### Autoscaling Group

- `AutoScalingGroup`: Creates an autoscaling group with the specified launch template, capacity settings, target group ARN, subnets, and tags.

### SNS Topic and CloudWatch Alarm

- `MySnsTopic`: Creates an SNS topic with an email subscription.
- `CpuUtilizationAlarm`: Creates a CloudWatch alarm for CPU utilization of the autoscaling group.

### CloudWatch Logs

- `LogGroup`: Creates a CloudWatch Logs log group with a specified retention period and tags.
- `LogStream`: Creates a CloudWatch Logs log stream within the log group.
- `MetricFilter`: Creates a metric filter to extract specific information from the log stream and generate CloudWatch metrics.
- `LogMetric`: Creates a CloudWatch metric for the filtered log events.

## Outputs

The template includes the following outputs:

- `LoadBalancerDNSName`: The DNS name of the load balancer.

## Usage

_This stack is currently set to work for the following regions: `eu-west-1`, `eu-west-2`, `us-east-1`, `us-west-1` (Edit the `RegionAMI` mapping accordingly with new regions and related AMIs, edit also the `AvailabilityZoneSubnets` mapping to use this stack in different regions)._

1. Make sure to have an IAM role to allow CloudFormation to create resources (if not, create one).
2. Upload the template (`main.yaml`) and application files (`app/` folder and content) to an S3 bucket.
3. Launch the CloudFormation stack and provide the necessary parameters [see [Parameters](#parameters) section above]
    * When providing the `URL` to upload the stack from the s3 bucket, follow this format: `https://<bucket-name>.s3-<region>.amazonaws.com/main.yaml`
4. Wait for the stack to complete and check the outputs for important information such as the load balancer DNS name.
5. Wait for the ec2 instances to be initialized and with `status check` -> `2/2 checks passed`
6. `curl` the `LoadBalancerDNS` provided in the Stack output

## Notes

- The template uses AWS resources that may incur costs. Make sure to review the pricing information for each resource before deploying the stack.
- The template assumes that you have an existing S3 bucket where the CloudFormation template and application files are stored. If not, you need to create one before launching the stack.
- The template provides basic security group rules for inbound access. Make sure to adjust these rules according to your specific requirements and best practices.
- The template uses default values for certain parameters, such as the instance type and operating system. You can modify these defaults in the CloudFormation parameters section.

