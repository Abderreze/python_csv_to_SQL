$compressItems = @(
    @{
        Path = "Tables/deces-2019.csv", "Tables/deces-2020.csv", "Tables/deces-2021.csv", "Tables/deces-2022.csv"
        DestinationPath = "zips/csv_deces2019-2022.zip"
    },
    @{
        Path = "Tables/deces-2023.csv", "Tables/deces-2024.csv"
        DestinationPath = "zips/csv_deces2023-2024.zip"
    },
    @{
        Path = "Tables/prenoms.db"
        DestinationPath = "zips/db.zip"
    }
)

foreach ($item in $compressItems) {
    Compress-Archive -Force -Path $item.Path -DestinationPath $item.DestinationPath
}
