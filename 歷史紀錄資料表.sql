USE [IoTDB]
GO

/****** Object:  Table [dbo].[HistoryRecord]    Script Date: 2024/2/26 ¤W¤È 01:17:12 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[HistoryRecord](
	[Number] [int] IDENTITY(1,1) NOT NULL,
	[UserID] [varchar](100) NOT NULL,
	[UserRecord] [nvarchar](50) NOT NULL,
	[CreateDate] [datetime] NULL,
 CONSTRAINT [PK_HistoryRecord_1] PRIMARY KEY CLUSTERED 
(
	[Number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[HistoryRecord] ADD  CONSTRAINT [DF_HistoryRecord_CreateDate]  DEFAULT (getdate()) FOR [CreateDate]
GO


