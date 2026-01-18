USE [IoTDB]
GO

/****** Object:  Table [dbo].[LinerUsers]    Script Date: 2024/2/26 上午 01:18:07 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[LinerUsers](
	[UserID] [varchar](100) NOT NULL,
	[DisplayName] [nvarchar](100) NOT NULL,
	[Language] [nvarchar](10) NOT NULL,
	[pictureURL] [varchar](150) NULL,
	[isActive] [bit] NULL,
	[CreateDate] [datetime] NULL,
 CONSTRAINT [PK_LinerUsers] PRIMARY KEY CLUSTERED 
(
	[UserID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[LinerUsers] ADD  CONSTRAINT [DF_LinerUsers_isActive]  DEFAULT ((1)) FOR [isActive]
GO

ALTER TABLE [dbo].[LinerUsers] ADD  CONSTRAINT [DF_LinerUsers_CreateDate]  DEFAULT (getdate()) FOR [CreateDate]
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Line User ID 具有唯一性' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'LinerUsers', @level2type=N'COLUMN',@level2name=N'UserID'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'使用者Line呈現名稱' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'LinerUsers', @level2type=N'COLUMN',@level2name=N'DisplayName'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Line使用者相片網址' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'LinerUsers', @level2type=N'COLUMN',@level2name=N'pictureURL'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'1-加入或解鎖 0-被封鎖' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'LinerUsers', @level2type=N'COLUMN',@level2name=N'isActive'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'新增日期' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'LinerUsers', @level2type=N'COLUMN',@level2name=N'CreateDate'
GO


