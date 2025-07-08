USE [DatabaseName];
GO

DECLARE @vcSQL VARCHAR(MAX) = ''

SELECT @vcSQL += 'SELECT * FROM dbo.' + NAME + ' UNION ALL '
	FROM sys.tables