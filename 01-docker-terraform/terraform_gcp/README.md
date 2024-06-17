# What terraform is?

HashiCorp terraform 是基礎架構即程式碼 (IaC) 工具，Infrastructure as Code 是一種自動化管理和佈署基礎設施的方法。將基礎設施定義編寫成程式碼，並使用自動化工具來佈署和管理基礎設施。可以對這些檔案進行版本控制、重複使用和共用。並使用一致的工作流程，來配置和管理所有基礎架構的整個生命週期。使用IaC進行雲端設施佈署，有下列的優點：

1. 減少手動佈署的失誤
    
    使用IaC配置雲端基礎設施，能夠降低手動佈署在操作上出現錯誤和延遲發生的機會。且能夠清楚快速地確定基礎設施狀態和配置，使整個過程更具可靠性和安全性。
    
2. 可重複性(reproducibility)
    
    此用IaC編寫的程式碼能夠被重複使用，消除手動佈署因人員操作導致結果產生的差異性。
    
3. 擴展性高(scalable)
    
    因為具有可重複性，所以在佈署時能快速擴展設施，減少系統建置時間和出錯的可能性。
    
4. 控制版本(version control)
    
    當需求產生變化時，改寫程式碼所產生的變化，可以使用IaC追蹤基礎設施的變化和配置，達到更輕鬆的管理。
    

使用Terraform將可以滿足雲端架構設計的四大面向：高可用性 High Availability、高擴展性 High scalability、高安全性 High Security、高靈活性 High Flexibility。

# Work Flow

如何執行寫好的雲端建設計畫

- Execution Steps
    - `terraform init` - 初始化 Terraform 環境
    - `terraform fmt` - 格式化 Terraform 程式碼。
    - `terraform validate` - 在建構計畫前驗證 Terraform 的語法和結構是否正確 。
    - `terraform plan` - 生成一個執行計畫，會比較 Terraform 文件與雲端的實際狀態，並列出預計創建、變更或刪除的資源。
    - `terraform apply` - 實際執行計畫
    - `terraform destroy` - 用於刪除由 Terraform 管理的所有資源，還原到初始狀態。
    - `terraform show` - 用於檢查建立完成的設施狀態

## Variables & Outputs

If you're familiar with traditional programming languages, it can be useful to compare Terraform modules to function definitions:

- Input variables are like function arguments.
- Output values are like function return values.
- Local values are like a function's temporary local variables.

### Input variables

Input variables let you customize aspects of Terraform modules without altering the module's own source code. This functionality allows you to share modules across different Terraform configurations, making your module composable and reusable.

**Declaring input variables**

Each input variable accepted by a module must be declared using a `variable` block:
**Arguments**

- [`default`](https://developer.hashicorp.com/terraform/language/values/variables#default-values) - A default value which then makes the variable optional.
- [`type`](https://developer.hashicorp.com/terraform/language/values/variables#type-constraints) - This argument specifies what value types are accepted for the variable.
- [`description`](https://developer.hashicorp.com/terraform/language/values/variables#input-variable-documentation) - This specifies the input variable's documentation.
- [`validation`](https://developer.hashicorp.com/terraform/language/values/variables#custom-validation-rules) - A block to define validation rules, usually in addition to type constraints.
- [`sensitive`](https://developer.hashicorp.com/terraform/language/values/variables#suppressing-values-in-cli-output) - Limits Terraform UI output when the variable is used in configuration.
- [`nullable`](https://developer.hashicorp.com/terraform/language/values/variables#disallowing-null-input-values) - Specify if the variable can be `null` within the module.

```python
variable "image_id" {
  type = string
}

variable "zone_names" {
  type    = list(string)
  default = ["us-west1"]
}

variable "docker_ports" {
  type = list(object({
    internal = number
    external = number
    protocol = string
  }))
  default = [
    {
      internal = 5432
      external = 5432
      protocol = "tcp"
    }
  ]
}
```

# Google Cloud Provider Documentation

[Terraform Registry](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

# Referrence

[Overview - Configuration Language | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language)

[Terraform 從零開始 - 實戰Lab打造GCP雲端自動化架構 :: 2023 iThome 鐵人賽](https://ithelp.ithome.com.tw/users/20104919/ironman/6605)