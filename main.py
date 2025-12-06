"""
ARTIFICIAL INTELLIGENCE PROJECT
People Dataset Preprocessing System
"""

import pandas as pd

class DataPreprocessor:
    """Main class for data preprocessing operations"""
    
    def __init__(self):
        self.dataset = None
        self.cleaned_data = None
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("DATA PREPROCESSING SYSTEM")
        print("="*60)
        print("\n1. Load Dataset")
        print("2. Explore Dataset")
        print("3. Analyze Data Quality")
        print("4. Clean Dataset")
        print("5. Export Cleaned Data")
        print("6. Exit")
        print("="*60)
    
    def load_dataset(self):
        """Load the dataset from CSV file"""
        print("\n[1] LOADING DATASET")
        print("-"*40)
        
        try:
            self.dataset = pd.read_csv("people-100000.csv")
            print("✅ Dataset loaded successfully!")
            print(f"   📊 Records: {len(self.dataset):,}")
            print(f"   📈 Columns: {len(self.dataset.columns)}")
             
            # Display column information
            print("\n   📋 Dataset Structure:")
            print("   " + "-"*35)
            for i, col in enumerate(self.dataset.columns, 1):
                print(f"   {i:2}. {col:15} ({self.dataset[col].dtype})")
            
            return True
        except FileNotFoundError:
            print("❌ Error: 'people-100000.csv' not found!")
            print("   Please ensure the file is in the same directory.")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def explore_dataset(self):
        """Explore and describe the dataset"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[2] DATASET EXPLORATION")
        print("-"*40)
        
        # Basic information
        print("\n📊 BASIC INFORMATION:")
        print(f"   • Total Records: {len(self.dataset):,}")
        print(f"   • Total Columns: {len(self.dataset.columns)}")
        print(f"   • Dataset Shape: {self.dataset.shape}")
        
        # Data types
        print("\n📝 DATA TYPES:")
        dtype_counts = self.dataset.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"   • {dtype}: {count} columns")
        
        # First few records
        print("\n👁️  SAMPLE DATA (First 3 records):")
        print(self.dataset.head(3).to_string(index=False))
        
        # Column statistics
        print("\n📈 COLUMN STATISTICS:")
        numeric_cols = self.dataset.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            print("   Numerical columns statistics:")
            for col in numeric_cols:
                print(f"   • {col}: Min={self.dataset[col].min()}, "
                      f"Max={self.dataset[col].max()}, "
                      f"Mean={self.dataset[col].mean():.2f}")
    
    def analyze_quality(self):
        """Analyze data quality issues"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[3] DATA QUALITY ANALYSIS")
        print("-"*40)
        
        issues = []
        
        # 1. Check for missing values
        print("\n🔍 MISSING VALUES ANALYSIS:")
        missing_data = self.dataset.isnull().sum()
        total_missing = missing_data.sum()
        
        if total_missing > 0:
            issues.append(f"Missing Values ({total_missing} total)")
            print(f"   ❌ Total missing values: {total_missing}")
            for col, count in missing_data.items():
                if count > 0:
                    percentage = (count / len(self.dataset)) * 100
                    print(f"      • {col}: {count} ({percentage:.1f}%)")
        else:
            print("   ✅ No missing values found")
        
        # 2. Check for duplicates
        print("\n🔍 DUPLICATE RECORDS ANALYSIS:")
        duplicates = self.dataset.duplicated().sum()
        
        if duplicates > 0:
            issues.append(f"Duplicate Records ({duplicates} found)")
            print(f"   ❌ Duplicate records: {duplicates}")
            
            # Show duplicate examples
            duplicate_rows = self.dataset[self.dataset.duplicated()]
            print(f"\n   📄 Example of duplicate records:")
            print(duplicate_rows.head(2).to_string(index=False))
        else:
            print("   ✅ No duplicate records found")
        
        # 3. Data type consistency
        print("\n🔍 DATA TYPE CONSISTENCY:")
        for col in self.dataset.columns:
            unique_count = self.dataset[col].nunique()
            if unique_count < 10:  # Low cardinality columns
                print(f"   • {col}: {unique_count} unique values")
        
        # Summary
        print("\n" + "="*40)
        print("QUALITY SUMMARY:")
        if issues:
            print("❌ Issues detected:")
            for issue in issues:
                print(f"   • {issue}")
        else:
            print("✅ Excellent data quality - No issues detected!")
        print("="*40)
    
    def clean_dataset(self):
        """Clean the dataset"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[4] DATA CLEANING PROCESS")
        print("-"*40)
        
        # Create a copy for cleaning
        self.cleaned_data = self.dataset.copy()
        
        print("Starting cleaning process...\n")
        
        # Step 1: Remove duplicates
        initial_count = len(self.cleaned_data)
        self.cleaned_data = self.cleaned_data.drop_duplicates()
        final_count = len(self.cleaned_data)
        duplicates_removed = initial_count - final_count
        
        if duplicates_removed > 0:
            print(f"✅ STEP 1: Removed {duplicates_removed} duplicate records")
        else:
            print("✅ STEP 1: No duplicates to remove")
        
        # Step 2: Handle missing values
        print("\n✅ STEP 2: Handling missing values")
        
        # Fill specific columns
        if 'Email' in self.cleaned_data.columns:
            email_missing = self.cleaned_data['Email'].isnull().sum()
            if email_missing > 0:
                self.cleaned_data['Email'] = self.cleaned_data['Email'].fillna('no-email@example.com')
                print(f"   • Filled {email_missing} missing emails")
        
        if 'Phone' in self.cleaned_data.columns:
            phone_missing = self.cleaned_data['Phone'].isnull().sum()
            if phone_missing > 0:
                self.cleaned_data['Phone'] = self.cleaned_data['Phone'].fillna('000-000-0000')
                print(f"   • Filled {phone_missing} missing phone numbers")
        
        # Fill remaining numeric columns with 0
        numeric_cols = self.cleaned_data.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            missing = self.cleaned_data[col].isnull().sum()
            if missing > 0:
                self.cleaned_data[col] = self.cleaned_data[col].fillna(0)
                print(f"   • Filled {missing} missing values in {col}")
        
        # Fill remaining text columns with 'Unknown'
        text_cols = self.cleaned_data.select_dtypes(include=['object']).columns
        for col in text_cols:
            if col not in ['Email', 'Phone']:
                missing = self.cleaned_data[col].isnull().sum()
                if missing > 0:
                    self.cleaned_data[col] = self.cleaned_data[col].fillna('Unknown')
                    print(f"   • Filled {missing} missing values in {col}")
        
        # Step 3: Data type standardization
        print("\n✅ STEP 3: Standardizing data formats")
        
        # Convert date columns if they exist
        date_columns = [col for col in self.cleaned_data.columns 
                       if 'date' in col.lower() or 'birth' in col.lower()]
        
        for col in date_columns:
            try:
                self.cleaned_data[col] = pd.to_datetime(self.cleaned_data[col], errors='coerce')
                print(f"   • Converted {col} to datetime format")
            except:
                pass
        
        # Summary
        print("\n" + "="*40)
        print("CLEANING COMPLETE!")
        print(f"Original records: {initial_count:,}")
        print(f"Cleaned records: {final_count:,}")
        print(f"Records removed: {duplicates_removed}")
        print("="*40)
        
        # Show cleaned data sample
        print("\n📄 CLEANED DATA SAMPLE:")
        print(self.cleaned_data.head(3).to_string(index=False))
    
    def export_data(self):
        """Export cleaned data to CSV"""
        if self.cleaned_data is None:
            print("❌ Please clean dataset first (Option 4)")
            return
        
        print("\n[5] EXPORT CLEANED DATA")
        print("-"*40)
        
        filename = "cleaned_people_dataset.csv"
        
        try:
            self.cleaned_data.to_csv(filename, index=False)
            
            print(f"✅ Data exported successfully!")
            print(f"\n📁 File Details:")
            print(f"   • Filename: {filename}")
            print(f"   • Records: {len(self.cleaned_data):,}")
            print(f"   • Columns: {len(self.cleaned_data.columns)}")
            print(f"   • File size: {len(self.cleaned_data) * len(self.cleaned_data.columns):,} data points")
            
            print(f"\n📍 File saved in current directory:")
            print(f"   {filename}")
            
            # Verify export
            print(f"\n🔍 Verification - First 2 records of exported file:")
            exported = pd.read_csv(filename)
            print(exported.head(2).to_string(index=False))
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def run(self):
        """Main program loop"""
        print("\n" + "="*60)
        print("WELCOME TO DATA PREPROCESSING SYSTEM")
        print("="*60)
        print("\nThis system will help you:")
        print("1. Load and explore your dataset")
        print("2. Analyze data quality issues")
        print("3. Clean and preprocess the data")
        print("4. Export cleaned data for analysis")
        print("="*60)
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.load_dataset()
            elif choice == '2':
                self.explore_dataset()
            elif choice == '3':
                self.analyze_quality()
            elif choice == '4':
                self.clean_dataset()
            elif choice == '5':
                self.export_data()
            elif choice == '6':
                print("\n" + "="*60)
                print("THANK YOU FOR USING DATA PREPROCESSING SYSTEM")
                print("="*60)
                break
            else:
                print("❌ Invalid choice! Please enter 1-6")
            
            input("\nPress Enter to continue...")

def main():
    """Main function"""
    processor = DataPreprocessor()
    processor.run()

if __name__ == "__main__":
    main()