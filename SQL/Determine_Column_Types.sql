USE [DatabaseName];
GO

DECLARE @TableName NVARCHAR(128) = 'YourTableName';  -- Replace with your table name
DECLARE @SQL NVARCHAR(MAX) = '';
DECLARE @ColumnName NVARCHAR(128);
DECLARE @DataType NVARCHAR(128);
DECLARE @MaxLength INT;

-- Table to store results
IF OBJECT_ID('tempdb..#DataTypeSuggestions') IS NOT NULL DROP TABLE #DataTypeSuggestions;
CREATE TABLE #DataTypeSuggestions (
    ColumnName NVARCHAR(128),
    SuggestedDataType NVARCHAR(128),
    Reason NVARCHAR(256)
);

DECLARE ColumnCursor CURSOR FOR
SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = @TableName AND DATA_TYPE = 'nvarchar';

OPEN ColumnCursor;
FETCH NEXT FROM ColumnCursor INTO @ColumnName;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- Check for INT
    SET @SQL = 'IF NOT EXISTS (SELECT 1 FROM ' + @TableName + ' WHERE ISNUMERIC(' + @ColumnName + ') = 0)
                BEGIN
                    INSERT INTO #DataTypeSuggestions (ColumnName, SuggestedDataType, Reason)
                    VALUES (''' + @ColumnName + ''', ''INT'', ''All values can be converted to INT'');
                END';
    EXEC(@SQL);
    
    -- Check for FLOAT (real or decimal)
    SET @SQL = 'IF NOT EXISTS (SELECT 1 FROM ' + @TableName + ' WHERE ISNUMERIC(' + @ColumnName + ') = 0)
                BEGIN
                    INSERT INTO #DataTypeSuggestions (ColumnName, SuggestedDataType, Reason)
                    VALUES (''' + @ColumnName + ''', ''FLOAT'', ''All values can be converted to FLOAT'');
                END';
    EXEC(@SQL);

    -- Check for DATE or DATETIME
    SET @SQL = 'IF NOT EXISTS (SELECT 1 FROM ' + @TableName + ' WHERE ISDATE(' + @ColumnName + ') = 0)
                BEGIN
                    INSERT INTO #DataTypeSuggestions (ColumnName, SuggestedDataType, Reason)
                    VALUES (''' + @ColumnName + ''', ''DATETIME'', ''All values can be converted to DATETIME'');
                END';
    EXEC(@SQL);
    
    -- Check for BIT (boolean)
    SET @SQL = 'IF NOT EXISTS (SELECT 1 FROM ' + @TableName + ' WHERE ' + @ColumnName + ' NOT IN (''0'', ''1''))
                BEGIN
                    INSERT INTO #DataTypeSuggestions (ColumnName, SuggestedDataType, Reason)
                    VALUES (''' + @ColumnName + ''', ''BIT'', ''All values are 0 or 1'');
                END';
    EXEC(@SQL);

    -- Determine max length
    SET @SQL = 'INSERT INTO #DataTypeSuggestions (ColumnName, SuggestedDataType, Reason)
                SELECT ''' + @ColumnName + ''', ''NVARCHAR('' + CAST(MAX(LEN(' + @ColumnName + ')) AS NVARCHAR(10)) + '')'', 
                       ''Max length determined to be '' + CAST(MAX(LEN(' + @ColumnName + ')) AS NVARCHAR(10))
                FROM ' + @TableName + ';
                ';
    EXEC(@SQL);

    FETCH NEXT FROM ColumnCursor INTO @ColumnName;
END

CLOSE ColumnCursor;
DEALLOCATE ColumnCursor;

-- Output the results
SELECT * FROM #DataTypeSuggestions;

-- Clean up
DROP TABLE #DataTypeSuggestions;
