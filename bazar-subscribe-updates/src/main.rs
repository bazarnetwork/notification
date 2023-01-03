use aws_sdk_dynamodb::Client;
use aws_sdk_dynamodb::model::AttributeValue;
use http::Response;
use lambda_http::IntoResponse;
use lambda_http::{lambda_runtime::Error, service_fn, Request, http::StatusCode};
use serde::Deserialize;
use serde::Serialize;
use serde_json::json;
use log::{info, error};


#[derive(Debug, Serialize, Deserialize)]
pub struct SubscribeUpdates {
    pub name: String,
    pub email: String,
    pub phone: String,
    pub message: String
}

#[derive(Debug, Serialize)]
struct SuccessResponse {
    pub body: String,
}

#[derive(Debug, Serialize)]
struct FailureResponse {
    pub body: String,
}

impl std::fmt::Display for FailureResponse {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.body)
    }
}

impl std::error::Error for FailureResponse {}

#[tokio::main]
async fn main() -> Result<(), Error> {
    info!("logger has been set up");
    tracing_subscriber::fmt::init();
    lambda_http::run(service_fn(handler)).await?;
    Ok(())
}

async fn handler(request: Request) -> Result<impl IntoResponse, Error> {
    info!("Handling a request, Request is: {:?}", request);

    let request_json = match request.body() {
        lambda_http::Body::Text(json_string) => json_string,
        _ => "",
    };    
    info!("Request JSON is : {:?}", request_json);
    let request_struct: SubscribeUpdates = serde_json::from_str(&request_json).map_err(|err| {
        error!("JSON doesnot have the expected structure, error: {}", err);
        FailureResponse {           
            body: "Incorrect JSON content. The lambda encountered an error and your record was not saved".to_owned(),
        }
    })?;

    let config = aws_config::load_from_env().await;
    let client = Client::new(&config);

    let name_av = AttributeValue::S(request_struct.name.clone());
    let email_av = AttributeValue::S(request_struct.email.clone());
    let phone_av = AttributeValue::S(request_struct.phone.clone());
    let message_av = AttributeValue::S(request_struct.message.clone());

    let _response = client.put_item()
        .table_name("dev_quarry_subscribe_updates")
        .item("name", name_av)
        .item("email", email_av)
        .item("phone", phone_av)
        .item("message", message_av)
        .send()
        .await
        .map_err(|err| {
            error!("failed to put item in dev_quarry_subscribe_updates table, error: {}", err);
            FailureResponse {
                body: "The lambda encountered an error and your record was not saved".to_owned(),
            }
        })?;

    info!("The record has been successfully stored: {:?}", &request_struct);

    let response = Response::builder()
        .status(StatusCode::OK)
        .header("Access-Control-Allow-Headers", "Content-Type")
        .header("Access-Control-Allow-Origin", "*")
        .header("Access-Control-Allow-Methods", "OPTIONS,POST,GET")
        .body(json!({
            "message": "The record has been successfully stored"
        }).to_string()).map_err(Box::new)?;

    Ok(response)
    
}