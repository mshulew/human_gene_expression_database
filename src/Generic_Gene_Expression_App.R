# Load libraries
library(readr)
library(shiny)
library(DT) # For interactive tables (you might use other libraries for plotting)

# Import FANTOM analysis
fantom_data <- read_tsv('C:/Users/Mark/Documents/Bio-Rad/FANTOM revisited/fantom_analysis.tsv',col_names=TRUE)
fantom_data <- as.data.frame(fantom_data)
rownames(fantom_data) <- fantom_data$GeneSymbol
fantom_data <- fantom_data[,-which(names(fantom_data) == "GeneSymbol")]
expression_data <- subset(fantom_data, select = -entrezgene_id)
gene_info <- subset(fantom_data, select=entrezgene_id)

# Define UI
ui <- fluidPage(
  titlePanel("Gene Expression Viewer"),
  sidebarLayout(
    sidebarPanel(
      selectizeInput("selected_genes", "Select Genes", choices = rownames(expression_data), multiple = TRUE)
    ),
    mainPanel(
      DTOutput("gene_expression"),
      tags$hr(),
      DTOutput("gene_info"),
      plotOutput("gene_barplot") # Add plot output for histograms
    )
  )
)

# Define server logic
server <- function(input, output, session) {
  
  observeEvent(input$selected_genes, {
    # If more than 4 genes are selected, keep only the first 4 selected genes
    print(input$selected_genes)
    print(input)
    if (length(input$selected_genes) > 4) {
      updated_selection <- input$selected_genes[1:4]
      updateSelectizeInput(session, "selected_genes", selected = updated_selection)
      message <- "Please select a maximum of 4 genes.\n"
      cat(message)
    }
  })
  
  # Render the table for the selected genes
  output$gene_expression <- renderDT({
    # Filter the data based on the selected genes
    selected_data <- expression_data[input$selected_genes, , drop = FALSE]
    data_table <- data.frame(Genes = rownames(selected_data), format(selected_data,digits=3))
    datatable(data_table, options = list(pageLength = 4), rownames = FALSE) # Adjust options as needed
  })
  
  # Render a second table
  output$gene_info <- renderDT({
    # Filter the data based on the selected genes
    selected_data <- gene_info[input$selected_genes, , drop = FALSE]
    data_table <- data.frame(Genes = rownames(selected_data),selected_data)
    datatable(data_table, options = list(pageLength = 4), rownames = FALSE)
  })
  
  # Render bar plots for selected genes
  output$gene_barplot <- renderPlot({
    # Check if any genes are selected
    if (length(input$selected_genes) > 0) {
      # Create a bar plot for each selected gene
      par(mfrow = c(ceiling(length(input$selected_genes) / 2), 2)) # Adjust layout as needed
      for (gene in input$selected_genes) {
        #bar_data <- expression_data[gene, ]
        expression_data[['entrezgene_id']] <- NULL
        bar_data <- as.vector(unlist(expression_data[gene,][1,]))
        par(mar = c(8, 5, 4, 2) + 0.1) 
        barplot(bar_data, names.arg = colnames(expression_data), 
                main = gene, ylab = "Expression Value", col = "skyblue", border = "black", las=2, cex.names = 0.8)
      }
    }
  })
}

# Run the application
shinyApp(ui = ui, server = server)
