#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QDebug>
#include <QFile>
#include <QFileDialog>
#include <QFileInfo>
#include <QMessageBox>
#include <QProcess>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , m_lastPath(qApp->applicationDirPath() + QDir::separator() + "..")
{
    ui->setupUi(this);
    ui->csvView->setModel(&m_model);
    connect(ui->pdfPb, &QPushButton::clicked, this, &MainWindow::onPdfClicked);
    connect(ui->csvPb, &QPushButton::clicked, this, &MainWindow::onCsvClicked);
    connect(ui->destPb, &QPushButton::clicked, this, &MainWindow::onDestClicked);
    connect(ui->generatePb, &QPushButton::clicked, this, &MainWindow::onGenerateClicked);
    connect(ui->pdfLe, &QLineEdit::textChanged, this, &MainWindow::checkGenerateEnabled);
    connect(ui->userTextLe, &QLineEdit::textChanged, this, &MainWindow::checkGenerateEnabled);
    connect(ui->csvLe, &QLineEdit::textChanged, this, &MainWindow::checkGenerateEnabled);
    connect(ui->destLe, &QLineEdit::textChanged, this, &MainWindow::checkGenerateEnabled);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::onPdfClicked()
{
    auto fileName = QFileDialog::getOpenFileName(this, tr("Pdf files"), m_lastPath, tr("Pdf Files (*.pdf)"));
    if (fileName.isEmpty())
    {
        return;
    }

    QFile file(fileName);
    if (!file.open(QFile::ReadOnly))
    {
        QMessageBox::warning(this, tr("Can't open file"), tr("Can't open file %1").arg(fileName));
        return;
    }
    m_lastPath = QFileInfo(fileName).absolutePath();
    ui->pdfLe->setText(fileName);
}

void MainWindow::onCsvClicked()
{
    auto fileName = QFileDialog::getOpenFileName(this, tr("Csv files"), m_lastPath, tr("Csv Files (*.csv)"));
    if (fileName.isEmpty())
    {
        return;
    }

    QFile file(fileName);
    if (!file.open(QFile::ReadOnly))
    {
        QMessageBox::warning(this, tr("Can't open file"), tr("Can't open file %1").arg(fileName));
        return;
    }
    m_lastPath = QFileInfo(fileName).absolutePath();
    ui->csvLe->setText(fileName);
    m_model.clear();
    while (file.bytesAvailable())
    {
        auto line = QString::fromUtf8(file.readLine());
        auto lineItems = line.split(',');
        QList<QStandardItem *> items;
        for(auto &item: lineItems)
        {
            item = item.trimmed();
            items << new QStandardItem(item);
        }
        m_model.appendRow(items);
    }
}

void MainWindow::onDestClicked()
{
    auto dirName = QFileDialog::getExistingDirectory(this, tr("Destination dir"), m_lastPath);
    if (dirName.isEmpty())
    {
        return;
    }

    QDir dir(dirName);
    if (!dir.exists())
    {
        QMessageBox::warning(this, tr("No dir"), tr("Directory doesn't exist %1").arg(dirName));
        return;
    }
    m_lastPath = dirName;
    ui->destLe->setText(dirName);
}

void MainWindow::onGenerateClicked()
{
    auto *p = new QProcess(this);
    p->setProcessChannelMode(QProcess::ForwardedChannels);
    connect(p, &QProcess::errorOccurred, [this, p](const auto &error){
        QMessageBox::warning(this, "Warning", tr("Error occured: %1").arg(error));
        p->deleteLater();
    });
    connect(p, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), [this, p](const auto &exitCode, const auto &exitStatus){
        if (exitCode == 0)
        {
            QMessageBox::information(this, "Finished", tr("Signed files should be ready"));
        }
        else
        {
            QMessageBox::warning(this, "Warning", tr("Exit code: %1\nExit status: %2").arg(exitCode).arg(exitStatus));
        }
        p->deleteLater();
    });

    const QStringList params = {scriptPath(),
                                ui->pdfLe->text(), ui->userTextLe->text(), ui->csvLe->text(),
                                ui->destLe->text(), QString::number(ui->posSb->value()),
                                ui->alignCb->currentText(), ui->pagesCb->currentText(),
                                ui->fontLe->text(), QString::number(ui->fontSizeSb->value()),};
    qDebug() << Q_FUNC_INFO << params;
    p->start("python", params);
}

void MainWindow::checkGenerateEnabled()
{
    ui->generatePb->setEnabled(!ui->pdfLe->text().isEmpty() &&
                               (!ui->csvLe->text().isEmpty() || !ui->userTextLe->text().isEmpty()) &&
                               !ui->destLe->text().isEmpty());
}

QString MainWindow::scriptPath() const
{
#ifdef Q_OS_LINUX
    return QStringLiteral("..") + QDir::separator() + "pdf_signature.py";
#else
    return QStringLiteral("..") + QDir::separator() + QStringLiteral("..") + QDir::separator() + "pdf_signature.py";
#endif

}

